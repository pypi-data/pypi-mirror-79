import json
import time

from demo.utils_redis import RedisUtils
from framework.strategies_manager import StrategiesManager

"""
####################################################
# 策略管理器使用例子

实时行情格式：
CFFEX,F,IF,2009,0,2020-09-04 13:51:00,4737.4,4737.4,4735.6,4735.6,0.0,118.0,0,0.0,0.0,0.0,0

0 exchangeNo
1 commodity_type_
2 commodityNo
3 contractNo
4 klType
5 dateTimeStamp
6 highPrice
7 openPrice
8 lowPrice
9 closePrice
10 lastClosePrice
11 volume
12 turnover
13 turnoverRate
14 pe
15 changeRate
16 timestamp

历史数据格式
{'time_key': '2020-07-21 14:53:00', 'open': 4659.2, 'high': 4659.8, 'low': 4657.4, 'close': 4658.8, 'volume': 326.0, 'code': 'CFFEX.IF2008', 'pe_ratio': 0, 'turnover_rate': 0, 'turnover': 0, 'last_close': 4659.2, 'change_rate': -0.0085851648}

####################################################
"""

ri = RedisUtils('./redis.conf')
ri.lookup_redist_info()

# 创建实例，参数可以不传
manager = StrategiesManager(configPath='./sconfig.conf', tempPath='./temp', isShowQuoteMsg=True)


def myAction01(data):
    """
    自定义函数
    :param data: 返回的行情数据，实时返回的是dict类型，历史返回的是逗号分隔的字符串
    :return:
    """
    print(f'_______> {data}')
    time.sleep(2)


def myAction02(data):
    """
    自定义操作
    :param data:
    实时行情数据字符串
    历史行情数据，字典类型
    :return:
    """
    print(f'&&&&&&> {data}')
    # rsp = manager.getHistory(stock_code='NYMEX_F_CL_2010', startTime='2020-08-17', endTime='2020-08-17', ktype='1Min')
    # print(rsp)
    # time.sleep(5)


def myAction03(data):
    print(f'*********> {data}')
    global ri
    if type(data) == dict:
        ri.push_list_value('test2', json.dumps(data, ensure_ascii=False))
    else:
        ri.push_list_value('test2', data)


# 注册自定义函数
manager.registAction(myAction01)
manager.registAction(myAction02)
manager.registAction(myAction03)

# 实时数据使用，支持内外盘合约
manager.runRealTime(stock_code='COMEX_F_GC_2012', ktype='1Min', isGetAllQuote=False)
# 历史数据回测使用，支持内外盘合约
# manager.runHistory(stock_code='NYMEX_F_CL_2010', startTime='2020-08-07', endTime='2020-08-17', ktype='1Min')

# manager.runRealTime(stock_code='CFFEX_F_IF_2009', ktype='1Min', getAllQuote=False)
# manager.runHistory(stock_code='CFFEX_F_IF_2009', startTime='2020-06-07', endTime='2020-08-17', ktype='1Min')
