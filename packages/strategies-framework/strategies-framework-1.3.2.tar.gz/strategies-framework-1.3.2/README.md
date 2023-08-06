**StrategiesManager**

# 这是一个策略回测库，支持内外盘期货历史回测跟实时回测两种模式

# 格式
- 行情回调数据格式（自定义回调函数中的data参数）
```json
{'time_key': '2020-07-21 14:53:00', 'open': 4659.2, 'high': 4659.8, 'low': 4657.4, 'close': 4658.8,'volume': 326.0, 'code': 'CFFEX.IF2008', 'pe_ratio': 0, 'turnover_rate': 0, 'turnover': 0,'last_close': 4659.2, 'change_rate': -0.0085851648}
```
- 持仓列表格式
```
['合约', '最新价', '持仓均价', '数量', '方向', '开平标志', '交易费', '滑点', '浮动盈亏', '订单时间', '账户余额', '描述']
```

- 下单记录列表格式
```
['合约', '最新价', '成交价', '数量', '方向', '开平标志', '交易费', '滑点', '订单时间', '账户余额', '描述']
```

# 例子1 StrategiesManager简单使用：
```python
import time
from framework.strategies_manager import StrategiesManager

def myAction1(data):
    """
    自定义函数
    :param data: 返回的行情数据，实时返回的是dict类型，历史返回的是逗号分隔的字符串
    :return: 
    """
    print(f'_______> {data}')
    # time.sleep(2)


def myAction2(data):
    """
    自定义操作
    :param data: 行情数据，字典类型
    {'time_key': '2020-07-21 14:53:00', 'open': 4659.2, 'high': 4659.8, 'low': 4657.4, 'close': 4658.8, 'volume': 326.0, 'code': 'CFFEX.IF2008', 'pe_ratio': 0, 'turnover_rate': 0, 'turnover': 0, 'last_close': 4659.2, 'change_rate': -0.0085851648}
    :return:
    """
    print(f'&&&&&&> {data}')
    # rsp = manager.getHistory(stock_code='NYMEX_F_CL_2010', startTime='2020-08-17', endTime='2020-08-17', ktype='1Min')
    # print(rsp)
    time.sleep(5)

# 创建实例，参数可以不传
manager = StrategiesManager(configPath='./sconfig.conf', tempPath='./temp', isShowQuoteMsg=True)

# 注册自定义函数
manager.registAction(myAction1)
manager.registAction(myAction2)

# 实时数据使用，支持内外盘合约
# manager.runRealTime(stock_code='COMEX_F_GC_2012', ktype='1Min', getAllQuote=True)
# 历史数据回测使用，支持内外盘合约
manager.runHistory(stock_code='NYMEX_F_CL_2010', startTime='2020-06-07', endTime='2020-08-17', ktype='1Min')
```
## 例子2 综合策略使用：
```python
from framework.strategies_manager import StrategiesManager
from framework.trader.trade_manager import Direction, OffsetFlag

# 创建实例，参数可以不传
s_manager = StrategiesManager(configPath='./sconfig.conf', tempPath='./temp', isShowQuoteMsg=False)

trade_m = s_manager.getTradeManager()
trade_m.check_in_money(100000)

current_time = ''
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
        if current_time != msg['time_key']: # 同一分钟内只操作一次
            rr1 = data[-2]
            # 当前一根K线是阳线，并且当前k线开盘价大于前一根阳线开盘价买入
            if rr1['open'] < rr1['close'] and msg['open'] > rr1['open']:
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
                log.info(f'买入：{trade_m.get_all_position()}')
        current_time = msg['time_key']


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

# 注册自定义函数
s_manager.registAction(func=myAction01, contract_tag=contract)
s_manager.registAction(func=myAction02, contract_tag=contract)

# 实时数据使用，支持内外盘合约 CFFEX_F_IF_2009
# s_manager.runRealTime(stock_code='COMEX_F_GC_2012', ktype='1Min', isGetAllQuote=False)
# 历史数据回测使用，支持内外盘合约
s_manager.runHistory(stock_code=contract, startTime='2020-09-14', endTime='2020-09-14', ktype='1Min')
```

## 注意：
    1) 可同时运行多个同类型（多个历史回测或多个实时模拟）回测，registAction的时候注意填入contract_tag参数区分不同合约的回调函数
    2) 合约统一格式,下划线分隔，全大写： 交易所_F_合约名_合约号。例如：NYMEX_F_IF_2009 
    3) 

## 更新日志
- 2020.09.16
    1) 修改模拟交易统计
    
- 2020.09.09
    1) 添加数据缓存，可以获取前几根K线数据，data = StrategiesManager.get_quote_temp('COMEX_F_GC_2012')
    2) 统一历史跟实时数据格式，返回字典类型
    
- 2020.09.07
    1) 添加行情数据管理器
    2) 添加模拟交易模块

- 2020.09.02
    1) 修改StrategiesManager可选输出行情参数
    2) 修改runRealTime可选获取全部行情参数
    
- 2020.08.26
    1) 支持zmq断线重连
    2) 添加自定义函数异常捕捉
    
- 2020.08.21
    1) 修改执行自定义方法为异步
    2) 修改实时数据订阅合约过滤

- 2020.08.20
    1) 历史回测数据缓存本地

- 2020.08.17
    1) 策略框架构建
    2) 添加获取历史记录接口