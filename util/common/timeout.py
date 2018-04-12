# 超时装饰器

import time, signal

def callback_default():
    '''默认回调函数'''
    raise RuntimeError

def set_timeout(num, callback=callback_default):
    '''超时装饰器
    - num: 超时时间
    - callback：回调函数
    '''
    def wrapper(func):

        def handle(signum, frame):
            raise RuntimeError
        
        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)
                signal.alarm(num)
                r = func(*args, **kwargs)
                signal.alarm(0)
                return r
            except RuntimeError:
                callback()
        
        return to_do

    return wrapper