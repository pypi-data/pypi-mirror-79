import traceback
from collections import defaultdict
from queue import Queue
from threading import Thread

from framework.log_handler import DefaultLogHandler


class klEvent:
    """
    K 线事件
    """

    def __init__(self, theme: str, data, is_async=True):
        """

        :param theme: 事件类型，字符串
        :param data: 数据内容，没指定类型，取出的时候要注意类型转换
        :param is_async: 是否异步,默认True,True是不阻塞其它事件执行
        """
        self.theme = theme
        self.data = data
        self.is_async = is_async


class EventEngine:
    """事件驱动引擎"""

    def __init__(self, logHandler=None):
        if logHandler is None:
            self._logHandler = DefaultLogHandler(filename='EventEngine.log')
        else:
            self._logHandler = logHandler
        """初始化事件引擎"""
        # 事件队列
        self.__queue = Queue()
        # 事件引擎开关
        self.__active = False

        # 事件引擎处理线程
        self.__thread = Thread(target=self.__run, name="EventEngine.__thread")

        # 事件字典，key 为时间， value 为对应监听事件函数的列表
        self.__handlers = defaultdict(list)
        self.__handlers_thread = []

    def __run(self):
        """启动引擎"""
        while self.__active or self.__queue.qsize() != 0:  # 执行完队列的元素才借宿
            try:
                event = self.__queue.get(block=True)
                if not self.__active or event.theme == 'exit-loop':
                    break
                # 检查该事件是否有对应的处理函数
                if event is None or event.theme not in self.__handlers:
                    continue
                if event.is_async:
                    # 一个事件一条线程处理
                    handle_thread = Thread(target=self.__process, name="event", args=(event,))
                    # self.__handlers_thread.append(handle_thread)
                    handle_thread.start()
                else:
                    self.__process(event)
            except Exception as e:
                self._logHandler.error(e.args)
                self._logHandler.error(traceback.print_exc())
        self._logHandler.debug('---> EventEngine loop stop')
        self.__active = False
        self.__thread = None

    def __process(self, event: klEvent):
        """事件处理"""
        # 若存在,则按顺序将时间传递给处理函数执行
        for handler in self.__handlers[event.theme]:
            try:
                handler(event.data)
            except Exception as e:
                self._logHandler.error(e.args)
                self._logHandler.error(traceback.print_exc())
        # TODO 回收线程资源
        # self.__handlers_thread.pop()

    def isActivate(self):
        """
        是否开启线程
        :return:
        """
        return self.__active or self.__queue.qsize() != 0

    def start(self) -> bool:
        """引擎启动"""
        self.__active = True
        if self.__thread is None:
            self.__thread = Thread(target=self.__run, name="EventEngine.__thread")
        if self.__thread.is_alive():
            self._logHandler.info('---> EventEngine 线程已存在')
            self.__thread.join()
            self.__thread = Thread(target=self.__run, name="EventEngine.__thread")
        self.__thread.start()
        self._logHandler.debug('---> EventEngine start loop.')
        return True

    def stop(self):
        """停止引擎"""
        self.__active = False
        self.__queue.put(klEvent(theme='exit-loop', data=''))
        if self.__thread is not None:
            self.__thread.join()
        self._logHandler.debug('---> EventEngine stop finished.')

    def register(self, theme, handler):
        """注册事件处理函数监听"""
        if handler not in self.__handlers[theme]:
            self.__handlers[theme].append(handler)

    def unregister(self, theme, handler):
        """注销事件处理函数"""
        handler_list = self.__handlers.get(theme)
        if handler_list is None:
            return
        if handler in handler_list:
            handler_list.remove(handler)
        if len(handler_list) == 0:
            self.__handlers.pop(theme)

    def put(self, event):
        self.__queue.put(event)

    @property
    def queue_size(self):
        return self.__queue.qsize()
