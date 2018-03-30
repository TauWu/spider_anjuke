# -*- coding: utf-8 -*-

# 日志文件操作模块

import logging
import sys
from .date import Time

class log_base(object):
    """日志服务

    """
    def __init__(self,logger_name):
        logger = logging.getLogger(logger_name)
        formater = logging.Formatter('PID:%(process)-5s %(asctime)s [%(name)s] \t%(message)s', '%Y/%m/%d %H:%M:%S')
        file_handler = logging.FileHandler("./log/spider_all_{date}.log".format(date=Time.now_date_str()))
        file_handler.setFormatter(formater)
        stream_handler = logging.StreamHandler(sys.stderr)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.setLevel(logging.INFO)
        self.logger = logger

    def err(self, log):
        self.logger.error("[ERR] %s"%log)

    def info(self, log):
        self.logger.info("[INF] %s"%log)

    def fatal(self, log):
        self.logger.fatal("[FTL] %s"%log)

    def warning(self, log):
        self.logger.warning("[WRN] %s"%log)

    def debug(self, log):
        self.logger.debug("[DBG] %s"%log)


def use_logger(level):
    '''使用日志的装饰器
    '''
    def decorator(func):
        logger = log_base(func.__name__)
        def _func(*args, **kwargs):
            '''使用本装饰器的函数要求为日志输出函数 同时要求函数的第一个参数是需要输出的日志'''
            
            if level == "info":
                logger.info(args[0])
            elif level == "debug":
                logger.debug(args[0])
            elif level == "warn":
                logger.warning(args[0])
            elif level == "err":
                logger.err(args[0])
            elif level == "fatal":
                logger.fatal(args[0])
            return func(*args)

        return _func
        
    return decorator

@use_logger(level="info")
def base_info(msg):
    pass

# 测试代码

@use_logger(level="err")
def foo(msg):
    print("将会打印日志 %s"%msg)

@use_logger(level="info")
def fo(msg):
    print("将会打印日志 %s"%msg)

if __name__ == "__main__":
    for i in range(1, 10):
        foo("This is %d test"%i)
    for i in range(1, 10):
        fo("This is %d info test"%i)