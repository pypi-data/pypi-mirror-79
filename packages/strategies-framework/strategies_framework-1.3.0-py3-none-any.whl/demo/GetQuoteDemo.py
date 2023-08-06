from framework.log_handler import DefaultLogHandler
from framework.quote_manager import QuoteManager

####################################################
# 行情管理器使用例子
####################################################

log = DefaultLogHandler(filename='GetQuoteDemo.log')
log.info('************** 获取行情数据例子 ***************')

# 创建一个QuoteManager实例
quoteM = QuoteManager(isShowQuoteMsg=False)

# 获取历史数据，不使用回调函数，直接拿返回值
# data = quoteM.getHistory(stock_code='COMEX_F_GC_2012', startTime='2020-06-07', endTime='2020-08-17', ktype='1Min')
# print(data)


# 注意 QuoteManager的自定义回调方法不能执行耗时操作，否则会影响下一步执行
def listener_fun(data):
    print(f'1min > {data}')


def listener_fun2(data):
    print(f'5min > {data}')

# 获取历史数据，使用回调函数，历史数据会一条一条模拟行情产生，回调自定义函数
quoteM.getHistory(stock_code='COMEX_F_GC_2012', startTime='2020-08-07', endTime='2020-08-17'
                  , ktype='1Min', fun_listener=listener_fun)

# 获取实时行情数据
# quoteM.getRealTimeKL(stock_code='CFFEX_F_IF_2009', ktype='1Min', fun_listener=listener_fun)
# quoteM.getRealTimeKL(stock_code='CFFEX_F_IF_2009', ktype='5Min', fun_listener=listener_fun2)

quoteM.stop()
