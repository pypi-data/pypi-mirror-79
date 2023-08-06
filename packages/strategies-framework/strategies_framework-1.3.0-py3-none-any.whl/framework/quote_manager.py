import json
import time
import traceback
from threading import Thread

import zmq

from framework.engine_event import EventEngine, klEvent
from framework.log_handler import DefaultLogHandler
from framework.utils import file2dict, select_pan_type, isKtypeRight
from framework.utils_requests import get_page_json


class QuoteManager:
    _remote_history_url = 'http://{}/gethistory?code={}&startTime={}&endTime={}&ktype={}'
    _finished = False
    _threads = {}
    _zmq_clients = {}
    _quote_temp = {}  # 行情缓存数据
    _max_quote_size = 500  # 行情缓存数据最大条数

    def __init__(self, event_loop: EventEngine = None, configPath='./sconfig.conf'
                 , tempPath='./temp', isShowQuoteMsg=True):
        self._getAllQuote = False
        self._config = file2dict(configPath)
        self._url_ip = self._config['remote_history_url']
        self._kl_real_time_addr_in = self._config['kl_real_time_addr_in']
        self._kl_real_time_addr_out = self._config['kl_real_time_addr_out']
        self._tempDir = tempPath
        self._isShowQuoteMsg = isShowQuoteMsg
        self._logHandler = DefaultLogHandler(filename='QuoteManager.log')
        self._logHandler.info('************** 行情管理器初始化 ***************')

        if event_loop is None:
            self._event_loop = EventEngine(self._logHandler)
        else:
            self._event_loop = event_loop
        self._event_loop.start()

    def getEventloop(self):
        """
        获取事件堆
        :return:
        """
        return self._event_loop

    def stop(self):
        self._finished = True
        for k in self._threads.keys():
            self._threads[k].join()
        self._threads.clear()
        for k in self._zmq_clients.keys():
            self._zmq_clients[k].close()

        self._event_loop.put(klEvent(theme='exit-loop', data=''))  # 发出停止信号
        while self._event_loop.isActivate():
            time.sleep(3)

        self._event_loop.stop()
        self._logHandler.debug('QuoteManager stop finished.')

    def registQuoteListener(self, fun_listener, key: str):
        if fun_listener is not None:
            self._event_loop.register(key, fun_listener)

    def getHistory(self, stock_code, startTime='', endTime='', ktype='', fun_listener=None):
        """
        获取合约历史数据
        :param stock_code:
        :param startTime:
        :param endTime:
        :param ktype:
        :param fun_listener: 行情数据回调函数
        :return:
        """
        if not isKtypeRight(ktype):
            self._logHandler.error(f'不支持的类型：{ktype}')
            return

        start = startTime.replace('-', '')
        end = endTime.replace('-', '')
        #
        import os
        if not os.path.exists(self._tempDir):
            os.makedirs(self._tempDir)
        #
        key = f'{stock_code}-{start}-{end}-{ktype}'
        filePath = f'{self._tempDir}/{key}.dat'
        data_list = None
        if os.path.exists(filePath):
            data_list = file2dict(filePath)
        #
        if data_list is None:
            url = self._remote_history_url.format(self._url_ip, stock_code, startTime, endTime, ktype)
            rsp = get_page_json(url)
            data_list = rsp['data']
            if len(data_list) == 0:
                self._logHandler.error(f'从网络获取历史数据返回为空,历史回测 {stock_code}合约 从{startTime}到{endTime} {ktype} 数据')
                return None

            # 转统一的合约格式
            for item in data_list:
                item['code'] = stock_code

            # 缓存到本地
            with open(filePath, 'w') as file:
                bJson = json.dumps(data_list, ensure_ascii=False)  # dict转json
                file.writelines(bJson)
                file.flush()

        # 注册事件监听回调函数
        self.registQuoteListener(fun_listener, key)

        if fun_listener is not None:
            if not self._event_loop.isActivate():
                self._event_loop.start()
            for item in data_list:
                self._event_loop.put(klEvent(theme=key, data=item, is_async=False))
        # for temp in data_list:
        #     self.save_quote_temp(stock_code, temp)
        return data_list

    def getRealTimeKL(self, stock_code: str, ktype: str, fun_listener, isGetAllQuote=False):
        """
        获取实时数据
        :param stock_code:
        :param ktype:
        :param fun_listener:
        :param isGetAllQuote: 是否获取所有订阅行情,默认False
        :return:
        """
        if not isKtypeRight(ktype):
            self._logHandler.error(f'不支持的类型：{ktype}')
            return

        key = f'{stock_code}-{ktype}'
        # 注册事件监听回调函数
        self.registQuoteListener(fun_listener, key)
        self._getAllQuote = isGetAllQuote

        if self._threads.get(key) is None:
            _watch_thread = Thread(target=self._doRealTimeAction, args=[stock_code, ktype],
                                   name=f'runRealTime-{stock_code}-{ktype}')
            self._threads[key] = _watch_thread
            _watch_thread.start()
        else:
            self._logHandler.error(f'已订阅合约：{stock_code}-{ktype}')

    def save_quote_temp(self, contract_name: str, data):
        """
        缓存行情数据
        :param contract_name:合约名，例如：NYMEX_F_IF_2009
        :param data:行情数据
        :return:
        """
        quote_list = self._quote_temp.get(contract_name)
        if quote_list is None:
            self._quote_temp[contract_name] = [data]
        else:
            last_data = quote_list[-1]
            # ll = str(last_data).split(',')
            # ll2 = data.split(',')
            # if ll[5] == ll2[5]:
            #     del quote_list[-1]
            #     quote_list.append(data)
            #     return

            if last_data['time_key'] == data['time_key']:
                quote_list[-1] = data
                return

            if len(quote_list) > self._max_quote_size:
                del quote_list[0]
            quote_list.append(data)

    def get_quote_temp(self, contract_name: str):
        """
        获取行情缓存数据列表
        :param contract_name: 合约名，例如：NYMEX_F_IF_2009
        :return:
        """
        quote_list = self._quote_temp.get(contract_name)
        return quote_list

    def _connect_zmq(self, stock_code, ktype):
        try:
            quote_ctx = zmq.Context()
            client = quote_ctx.socket(zmq.SUB)
            # client.setsockopt(zmq.ZMQ_RECONNECT_IVL, 500)
            # client.setsockopt(zmq.ZMQ_RECONNECT_IVL_MAX, 5000)

            pan_type = select_pan_type(stock_code)
            # 请求历史数据
            if pan_type == 'in':
                client.connect(self._kl_real_time_addr_in)
            elif pan_type == 'out':
                client.connect(self._kl_real_time_addr_out)
            else:
                self._logHandler.info("无法判断内外盘")
                return None

            client.setsockopt_string(zmq.SUBSCRIBE, ktype)
            client.setsockopt(zmq.RCVTIMEO, 10000)
            return client
        except zmq.error.ZMQError as e:
            self._logHandler.error("zmq 连接出错:%s" % e)
            return None

    def _doRealTimeAction(self, stock_code, ktype):
        self._logHandler.info(f'开启任务 ---> \n实时模拟 {stock_code}合约 {ktype} 数据')
        client = self._connect_zmq(stock_code, ktype)
        key = f'{stock_code}-{ktype}'
        if self._zmq_clients.get(key) is not None:
            try:
                self._zmq_clients.get(key).close()
            except Exception as e:
                self._logHandler.error(e.args)
                self._logHandler.error(traceback.print_exc())

        self._zmq_clients[key] = client

        while not self._finished:
            try:
                if client is not None:
                    response = client.recv()
                else:
                    self._logHandler.error(f'zmq尝试重连......')
                    client = self._connect_zmq(stock_code, ktype)
                    continue
            except zmq.ZMQError as e:
                self._logHandler.error(f'zmq {e.args}')

                client.close()
                self._logHandler.error(f'zmq尝试重连......')
                client = self._connect_zmq(stock_code, ktype)
                continue

            response = str(response, encoding='GB2312')
            if response != ktype:
                if self._isShowQuoteMsg:
                    self._logHandler.debug(response)
                response_list = response.split(',')
                rst = {}
                rst['time_key'] = response_list[5]
                rst['open'] = response_list[7]
                rst['high'] = response_list[6]
                rst['low'] = response_list[8]
                rst['close'] = response_list[9]
                rst['volume'] = response_list[11]
                rst['code'] = f'{response_list[0]}_{response_list[1]}_{response_list[2]}_{response_list[3]}'
                rst['pe_ratio'] = response_list[14]
                rst['turnover_rate'] = response_list[13]
                rst['turnover'] = response_list[12]
                rst['last_close'] = response_list[10]
                rst['change_rate'] = response_list[15]

                if self._getAllQuote \
                        or (rst['code'] == stock_code):
                    self._event_loop.put(klEvent(theme=key, data=response))

                # 缓存
                self.save_quote_temp(rst['code'].upper(), rst)

        # 结束循环，销毁订阅
        if self._zmq_clients.get(key) is not None:
            try:
                self._zmq_clients.get(key).close()
            except Exception as e:
                self._logHandler.error(e.args)
                self._logHandler.error(traceback.print_exc())
            self._zmq_clients.pop(key)
        self._logHandler.info(f'完成 {stock_code}合约 {ktype} 数据实时模拟任务')
