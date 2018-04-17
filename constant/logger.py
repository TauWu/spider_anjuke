from util.common.logger import use_logger

@use_logger(level="info")
def base_info(msg):
    pass

@use_logger(level="warn")
def base_warn(msg):
    pass

@use_logger(level="err")
def base_err(msg):
    pass

@use_logger(level="fatal")
def db_fatal(msg):
    pass

@use_logger(level="err")
def db_err(msg):
    pass

@use_logger(level="info")
def db_info(msg):
    pass

@use_logger(level="warn")
def db_warn(msg):
    pass

@use_logger(level="warn")
def req_warn(msg):
    pass

@use_logger(level="info")
def req_info(msg):
    pass

@use_logger(level="error")
def req_err(msg):
    pass

@use_logger(level="info")
def redis_info(msg):
    pass

@use_logger(level="err")
def redis_err(msg):
    pass