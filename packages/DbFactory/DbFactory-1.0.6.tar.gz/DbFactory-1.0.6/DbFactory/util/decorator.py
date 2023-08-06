# coding:utf-8
# author caturbhuja
# date   2020/8/31 5:10 下午 
# wechat chending2012 

# python pack
from functools import wraps
import time
import signal
import traceback


def cost_time(log_cost_time=False, warning_time=60, log=None, request_id=''):
    """
    :param log_cost_time: 打印函数花费时间到日志
    :param warning_time: 操作耗时告警时间
    :param log: 日志 实例 接入
    :param request_id: 消息 id 用于追踪上下文日志
    :return:
    """

    def wrap(function):
        """"""

        @wraps(function)
        def cost(*args, **kwargs):
            st = int(time.time())
            res = function(*args, **kwargs)
            et = int(time.time())
            ct = et - st
            if ct >= warning_time:
                message = "request {}, Db Client Function < {} > cost too long: {}s".format(request_id,
                                                                                            function.__name__, ct)
                if log:
                    log.warning(message)
                else:
                    print(message)
            if log_cost_time:
                message = "request {}, Function < {} > cost : {}s".format(request_id, function.__name__, ct)
                if log:
                    log.warning(message)
                else:
                    print(message)
            return res

        return cost

    return wrap


def time_out(interval=60, log=None):
    def decorator(func):
        def handler(signum, frame):
            raise SelfTimeoutError("GG simada! run func timeout ")

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(interval)  # interval秒后向进程发送SIGALRM信号
                result = func(*args, **kwargs)
                signal.alarm(0)  # 函数在规定时间执行完后关闭alarm闹钟
                return result
            except SelfTimeoutError as e:
                log.error(traceback.format_exc(3, e))

        return wrapper

    return decorator


# 自定义超时异常
class SelfTimeoutError(Exception):
    def __init__(self, msg):
        super(SelfTimeoutError, self).__init__()
        self.msg = msg


def try_and_reconnect(function, reconnect_obj, log=None, request_id=''):
    """
    待测试。使用可能性不大！
    这个装饰器，负责尝试连接，如果报错，则重新连接，
    :param function: 函数方法
    :param reconnect_obj: 重新连接 class 的函数方法
    :param log: 日志 实例 接入
    :param request_id: 消息 id 用于追踪上下文日志
    :return:
    """

    @wraps(function)
    def cost(*args, **kwargs):
        try:
            res = function(*args, **kwargs)
        except Exception as e:
            message = "request {}, retry reconnect, error info is {}".format(request_id, e)
            if log:
                log.warning(message)
            else:
                print(message)
            res = function(*args, **kwargs)
        return res

    return cost


if __name__ == '__main__':
    # @cost_time(warning_time=1)
    # def test_ggg():
    #     time.sleep(1)
    # test_ggg()

    # ---------- time_out test --------
    import logging

    logging.basicConfig(level=logging.DEBUG)


    @time_out(2, log=logging)
    def task1():
        print("task1 start")
        time.sleep(3)
        print("task1 end")


    @time_out(2, log=logging)
    def task2():
        print("task2 start")
        time.sleep(1)
        print("task2 end")


    task1()
    task2()
