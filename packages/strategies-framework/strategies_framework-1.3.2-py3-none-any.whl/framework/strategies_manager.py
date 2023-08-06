import json
import os
import traceback
from queue import Empty, Queue
from threading import Thread
import zmq
from framework.engine_event import EventEngine, klEvent
from framework.log_handler import DefaultLogHandler
from framework.trader.trade_manager import TradeManager
from framework.utils import file2dict, select_pan_type, isKtypeRight
from framework.utils_requests import get_page_json


class ActionFun:
    """
    用户自定义函数封装
    """
    typeName = ''  # 函数名
    fun = None  # 执行的函数
    tag = ''  # 对应的合约
    threadId = None  # 执行线程


class StrategiesManager:
    _remote_history_url = 'http://{}/gethistory?code={}&startTime={}&endTime={}&ktype={}'
    _threads = {}
    _finished = False
    _action = []
    _tempDir = './temp'
    _prepareActionQueue = Queue()
    _getAllQuote = False
    _quote_temp = {}  # 行情缓存数据
    _max_quote_size = 500  # 行情缓存数据最大条数
    _zmq_clients = {}  # zmq连接

    def __init__(self, configPath='./sconfig.conf', tempPath='./temp', isShowQuoteMsg=True):
        """
        初始化

        配置文件格式：
        {
            "remote_history_url": "127.0.0.1:10039",
            "kl_real_time_addr_in": "tcp://127.0.0.1:10019",
            "kl_real_time_addr_out": "tcp://127.0.0.1:10020"
        }
        :param configPath: 配置文件路径，默认./sconfig.conf
        :param tempPath: 数据缓存文件夹路径，默认./temp
        :param isShowQuoteMsg: 是否输出行情数据，默认True
        """
        self._logHandler = DefaultLogHandler(filename='strategies.log')
        self._logHandler.info('************** 策略管理器初始化 ***************')
        self._config = file2dict(configPath)
        self._url_ip = self._config['remote_history_url']
        self._kl_real_time_addr_in = self._config['kl_real_time_addr_in']
        self._kl_real_time_addr_out = self._config['kl_real_time_addr_out']
        self._tempDir = tempPath
        self._isShowQuoteMsg = isShowQuoteMsg

        self._eventloop = EventEngine(self._logHandler)
        self._eventloop.start()

        self._trade_m = TradeManager(event_loop=self._eventloop)

    def stop(self):
        self._logHandler.debug('---> StrategiesManager stopping...')
        self._finished = True

        for k in self._threads.keys():
            try:
                self._threads[k].join()
            except Exception as e:
                self._logHandler.error(e.args)
                self._logHandler.error(traceback.print_exc())
        self._threads.clear()

        for k in self._zmq_clients.keys():
            self._zmq_clients[k].close()
        self._eventloop.stop()
        self._logHandler.debug('---> StrategiesManager stop finished.')

    def getTradeManager(self):
        """
        获取交易管理器
        :return:
        """
        return self._trade_m

    def getEventloop(self):
        """
        获取事件堆
        :return:
        """
        return self._eventloop

    def registAction(self, func, contract_tag: str):
        """
        注册回调方法
        :param func:回调函数
        :param contract_tag:标记触发的合约，例如：NYMEX_F_CL_2009
        :return:
        """
        af = ActionFun()
        af.typeName = func.__name__
        af.tag = contract_tag
        af.fun = func
        self._action.append(af)

    def getHistory(self, stock_code, startTime='', endTime='', ktype='') -> dict:
        """
        获取合约历史数据
        :param stock_code:
        :param startTime:
        :param endTime:
        :param ktype:
        :return:
        """
        url = self._remote_history_url.format(self._url_ip, stock_code, startTime, endTime, ktype)
        rsp = get_page_json(url)
        return rsp

    def _doHistoryAction(self, stock_code, startTime='', endTime='', ktype=''):
        self._logHandler.info(f'开启任务 ---> 历史回测 {stock_code}合约 从{startTime}到{endTime} {ktype} 数据')
        self._logHandler.info('正在加载数据，请稍后...')

        if not isKtypeRight(ktype):
            self._logHandler.error(f'不支持的类型：{ktype}')
            return

        if not os.path.exists(self._tempDir):
            os.makedirs(self._tempDir)

        start = startTime.replace('-', '')
        end = endTime.replace('-', '')
        filename = f'{stock_code}-{start}-{end}-{ktype}'
        filePath = f'{self._tempDir}/{filename}.dat'
        data_list = None
        # 优先加载本地缓存
        if os.path.exists(filePath):
            data_list = file2dict(filePath)
        # 本地没有缓存从网络获取
        if data_list is None:
            url = self._remote_history_url.format(self._url_ip, stock_code, startTime, endTime, ktype)
            rsp = get_page_json(url)
            if len(rsp) == 0:
                self._logHandler.error(f'获取 {stock_code} 合约行情出错!!')
                return
            data_list = rsp['data']
            if len(data_list) == 0:
                self._logHandler.error(f'从网络获取历史数据返回为空,历史回测 {stock_code}合约 从{startTime}到{endTime} {ktype} 数据')
                return

            # 转统一的合约格式
            for item in data_list:
                item['code'] = stock_code

            # 缓存到本地
            with open(filePath, 'w') as file:
                bJson = json.dumps(data_list, ensure_ascii=False)  # dict转json
                file.writelines(bJson)
                file.flush()

        self._logHandler.info('加载数据完成，执行回测...')
        for item in data_list:
            self._eventloop.put(klEvent(theme=f'{stock_code}-{ktype}', data=item))
            # 缓存内存
            self._save_quote_temp(item['code'].upper(), item)

            # 执行回调函数
            for act in self._action:
                if act.tag == stock_code:
                    act.fun(item)

        key = stock_code + startTime + endTime + ktype
        self._threads.pop(key)
        self._trade_m.save_data()
        self._logHandler.info(f'完成任务 {filename} --->')
        if len(self._threads.keys()) == 0:
            self.stop()

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
        self._logHandler.info(f'开启任务 ---> 实时模拟 {stock_code}合约 {ktype} 数据')
        client = self._connect_zmq(stock_code, ktype)

        key = f'{stock_code}-{ktype}'
        if self._zmq_clients.get(key) is not None:
            try:
                self._zmq_clients.get(key).close()
            except Exception as e:
                self._logHandler.error(e.args)
                self._logHandler.error(traceback.print_exc())
        self._zmq_clients[key] = client

        for action in self._action:
            if action.tag == stock_code:
                self._prepareActionQueue.put(action)

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
                    self._logHandler.info("quote >:  {}".format(response))

                response_list = response.split(',')
                rst = {'time_key': response_list[5], 'open': response_list[7], 'high': response_list[6],
                       'low': response_list[8], 'close': response_list[9], 'volume': response_list[11],
                       'code': f'{response_list[0]}_{response_list[1]}_{response_list[2]}_{response_list[3]}',
                       'pe_ratio': response_list[14], 'turnover_rate': response_list[13], 'turnover': response_list[12],
                       'last_close': response_list[10], 'change_rate': response_list[15]}

                self._eventloop.put(klEvent(theme=f'{stock_code}-{ktype}', data=rst))
                # 缓存
                self._save_quote_temp(rst['code'].upper(), rst)

                if self._getAllQuote \
                        or (rst['code'] == stock_code):
                    size = self._prepareActionQueue.qsize()
                    while size != 0:
                        size -= 1
                        if not self._prepareActionQueue.empty():
                            try:
                                doact = self._prepareActionQueue.get(block=False)
                                if doact is not None:
                                    handle_thread = Thread(target=self._wraperFun, name=doact.typeName,
                                                           args=(doact, rst))
                                    doact.threadId = handle_thread
                                    handle_thread.start()
                            except Empty as e:
                                self._logHandler.error(f'{e.args}')
        # 结束循环，销毁订阅
        if self._zmq_clients.get(key) is not None:
            try:
                self._zmq_clients.get(key).close()
            except Exception as e:
                self._logHandler.error(e.args)
                self._logHandler.error(traceback.print_exc())
            self._zmq_clients.pop(key)

        self._threads.pop(key)
        self._trade_m.save_data()
        self._logHandler.info(f'完成任务 {key}--->')
        if len(self._threads.keys()) == 0:
            self.stop()

    def _wraperFun(self, doactfun, data):
        if isinstance(doactfun, ActionFun):
            try:
                doactfun.fun(data)
            except Exception as e:
                self._logHandler.error(f'执行任务<{doactfun.typeName}>发生异常：{e.args}')
                self._logHandler.error(traceback.print_exc())
            doactfun.threadId = None
            self._prepareActionQueue.put(doactfun)

    def _save_quote_temp(self, contract_name: str, data):
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
            if last_data['time_key'] == data['time_key']:
                # del quote_list[-1]
                # quote_list.append(data)
                quote_list[-1] = data
                return

            if len(quote_list) > self._max_quote_size:
                del quote_list[0]
            quote_list.append(data)
            # self._logHandler.debug(f'合约{contract_name}当前缓存条数：{len(quote_list)}')

    def get_history_quote(self, contract_name: str):
        """
        获取行情缓存数据列表
        :param contract_name: 合约名，例如：NYMEX_F_IF_2009
        :return:
        """
        quote_list = self._quote_temp.get(contract_name)
        # self._logHandler.debug(f'合约{contract_name}当前缓存条数：{len(quote_list)}')
        return quote_list

    def runRealTime(self, stock_code, ktype='1Min', isGetAllQuote=False):
        """
        运行实时数据模拟
        :param stock_code:例如：COMEX_F_GC_2012
        :param ktype: k线类型，默认1Min，例如：1Min
        :param isGetAllQuote:是否获取所有合约行情
        :return:
        """
        if stock_code == "":
            self._logHandler.error('合约信息为空，请输入合约代码')
            return
        self._getAllQuote = isGetAllQuote
        key = stock_code + ktype
        if self._threads.get(key) is None:
            self._threads[key] = Thread(target=self._doRealTimeAction, args=[stock_code, ktype], name="runRealTime")
            self._threads[key].start()
        else:
            self._logHandler.info('任务已存在 --->')

    def runHistory(self, stock_code, startTime='', endTime='', ktype='1Min'):
        """
        运行历史回测
        :param stock_code:
        :param startTime:
        :param endTime:
        :param ktype:
        :return:
        """
        key = stock_code + startTime + endTime + ktype
        if self._threads.get(key) is None:
            self._threads[key] = Thread(target=self._doHistoryAction, args=[stock_code, startTime, endTime, ktype],
                                        name="runHistory")
            self._threads[key].start()
        else:
            self._logHandler.info('任务已存在 --->')
