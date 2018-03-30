# -*- coding: utf-8 -*-

## 这一级目录下需要有一个数据库配置文件 config.py

# 待连接数据库基础信息

'''
database_info = {
    "host":"localhost",
    "port":3306,
    "user":"user",
    "passwd":"passwd",
    "db":"database",
    "charset":"utf8"
}
'''

from util.common.logger import use_logger

@use_logger(level="warn")
def db_warning(msg):
    pass

class DBController():
    """
    数据库操作模块
    
    可访问成员（函数）：
    - cur
    - IntegrityError
    - execute(sql)
    - close

    """

    def __init__(self, host="localhost", user="root", passwd="root", port=3306, db="spider_anjuke"):
        import pymysql
        from pymysql.err import IntegrityError

        try:
            from .config import database_info
            host=database_info["host"]
            port=database_info["port"]
            user=database_info["user"]
            passwd=database_info["passwd"]
            db=database_info["db"]
        except ImportError:
            db_warning("没有找到数据库配置文件，将以默认方法创建连接")

        # 保护连接为私有成员
        self._conn = pymysql.connect(host=host,port=port,user=user, passwd=passwd,db=db,charset='utf8')
        self.cur = self._conn.cursor()
        self.IntegrityError = IntegrityError

    def execute(self, SQL):
        # 执行一条SQL语句
        self.cur.execute(SQL)
        self._conn.commit()

    @property
    def close(self):
        # 关闭数据库连接
        self._conn.close()
        self.cur.close()