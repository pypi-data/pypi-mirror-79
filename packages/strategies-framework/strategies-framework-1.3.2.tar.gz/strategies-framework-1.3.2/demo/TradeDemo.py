from framework.log_handler import DefaultLogHandler
from framework.strategies_manager import StrategiesManager
from framework.trader.trade_manager import Direction, OffsetFlag

####################################################
# 交易管理器使用例子
# 持仓列表格式：
# [合约，最新价，持仓均价，数量，方向，开平标志，交易费，滑点，浮动盈亏，订单时间, 账户余额，描述]
#
# 订单历史记录格式：
# ['合约', '最新价', '成交价', '数量', '方向', '开平标志', '交易费', '滑点', '订单时间', '账户余额', '描述']
#
# 策略管理器跟交易管理器结合使用
####################################################

log = DefaultLogHandler(filename='TradeDemo.log')
log.info('************** 综合交易例子 ***************')

# 创建实例，参数可以不传
s_manager = StrategiesManager(configPath='./sconfig.conf', tempPath='./temp', isShowQuoteMsg=False)

trade_m = s_manager.getTradeManager()
trade_m.check_in_money(100000)

current_time = ''

# contract = 'COMEX_F_GC_2012'
# contract = 'NYMEX_F_IF_2009'
# contract = 'NYMEX_F_CL_2010'
contract = 'HKEX_F_HSI_2009'


def myAction01(msg):
    global s_manager
    global trade_m
    global log
    global contract
    log.info(msg)
    data = s_manager.get_history_quote(contract)
    if data is not None and len(data) > 2:
        global current_time
        if current_time != msg['time_key']:
            rr2 = data[-3]
            rr1 = data[-2]
            if rr1['open'] < rr1['close'] and rr2['close'] > rr2['open'] and rr1['open'] >= rr2['open']:
                """
                手续费计算分2种情况：
                （1）固定手续费
                    N手期货固定手续费 = N手*固定手续费
                （2）比例手续费
                    N手期货固定手续费 = N手*价格*交易单位*费率
                """
                trade_m.order(contract=contract
                              , money=float(msg['close'])
                              , volume=1
                              , orderDate=msg['time_key']
                              , direction=Direction.TM_BUY
                              , offset_flag=OffsetFlag.TM_Open
                              , transferfee=20 * 1
                              , slip=0)
                # log.info(f'账户余额：{trade_m.get_account_msg()}')
                log.info(f'买入：{trade_m.get_all_position()}')
        current_time = msg['time_key']


def myAction011(msg):
    global s_manager
    global trade_m
    global log
    global contract
    log.info(msg)
    data = s_manager.get_history_quote(contract)
    if data is not None and len(data) > 1:

        rr1 = data[-2]  # 前一根K线
        if rr1['open'] < rr1['close'] and msg['open'] > rr1['open']:
            trade_m.order(contract=contract
                          , money=float(msg['open'])
                          , volume=1
                          , orderDate=msg['time_key']
                          , direction=Direction.TM_BUY
                          , offset_flag=OffsetFlag.TM_Open
                          , transferfee=20 * 1
                          , slip=0)
            log.info(f'买入：{trade_m.get_all_position()}')


def myAction02(msg):
    """
    风控
    :param msg:
    msg 数据格式
    :return:
    """
    global trade_m
    global log
    global contract

    # 获取合约持仓
    position = trade_m.get_position(contract=contract
                                    , direction=Direction.TM_BUY
                                    , offset_flag=OffsetFlag.TM_Open)
    # 如果有持仓，且不是该行情时间成交的（实时行情是存在同分钟推送几次的问题，不在同一分钟内同时执行买卖操作）
    if position is not None: #  and msg['time_key'] != position[9]
        # 持仓数据格式：
        # [0 合约，1 最新价，2 持仓均价，3 数量，4 方向，5 开平标志，6 交易费，7 滑点，8 浮动盈亏，9 订单时间, 10 账户余额，11 描述]
        pre = round((float(msg['close']) - float(position[2])) / float(position[2]) * 100, 2)
        # pre = round((float(msg['close']) - float(msg['last_close'])) / float(msg['last_close']) * 100, 2)

        log.info(f'涨跌幅:{pre}')
        if pre >= 0.07 or pre < 0:  # 止盈止损，涨跌幅超过 1%
            log.info(f'################################')
            log.info(f'持仓：{position}')
            trade_m.order(contract=contract
                          , money=float(msg['close'])
                          , volume=int(position[3])
                          , orderDate=msg['time_key']
                          , direction=Direction.TM_SELL
                          , offset_flag=OffsetFlag.TM_Close
                          , transferfee=20 * int(position[3])
                          , slip=0)
            log.info(f'################################')


def myAction03(msg):
    print(msg)


# 注册自定义函数
# s_manager.registAction(func=myAction01, contract_tag=contract)
s_manager.registAction(func=myAction02, contract_tag=contract)
s_manager.registAction(func=myAction011, contract_tag=contract)

# s_manager.registAction(func=myAction03, contract_tag='COMEX_F_GC_2012')

# 实时数据使用，支持内外盘合约 CFFEX_F_IF_2009
# s_manager.runRealTime(stock_code=contract, ktype='1Min', isGetAllQuote=False)
# 历史数据回测使用，支持内外盘合约
s_manager.runHistory(stock_code=contract, startTime='2020-09-14', endTime='2020-09-14', ktype='1Min')

# 可同时运行多个同类型（多个历史回测或多个实时模拟）回测，registAction的时候注意填入contract_tag参数区分不同合约的回调函数
# 注意：暂不支持同一个StrategiesManager实例历史回测跟实时模拟同时使用
# s_manager.runHistory(stock_code='COMEX_F_GC_2012', startTime='2020-09-10', endTime='2020-09-10', ktype='1Min')
