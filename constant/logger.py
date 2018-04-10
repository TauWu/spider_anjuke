from util.common.logger import use_logger

@use_logger(level="err")
def db_err(msg):
    pass

@use_logger(level="info")
def db_info(msg):
    pass

@use_logger(level="warn")
def db_warning(msg):
    pass