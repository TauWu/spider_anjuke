# -*- coding: utf-8 -*-

from constant.logger import *
from util.config import ConfigReader

class DBController():
    """
    数据库操作模块
    
    可访问成员（函数）：
    - cur
    - IntegrityError
    - execute(sql)
    - close

    """

    def __init__(self, section_name="database"):
        import pymysql
        from pymysql.err import IntegrityError

        (host, port, user, passwd, db) = ConfigReader.read_section_keylist(section_name,[
            "host", "port", "user", "passwd", "db"])

        # 保护连接为私有成员
        try:
            self._conn = pymysql.connect(host=host, port=int(port), user=user, passwd=passwd, db=db, charset='utf8')
        except Exception:
            db_fatal("数据库连接创建失败！[%s:%s@%s:%s?charset=%s/%s]"%(user, passwd, host, port, "utf-8", db))
        self.cur = self._conn.cursor()
        self.IntegrityError = IntegrityError
        db_info("数据库连接创建成功！[%s:%s@%s:%s?charset=%s/%s]"%(user, passwd, host, port, "utf-8", db))

    def execute(self, SQL):
        # 执行一条SQL语句
        self.cur.execute(SQL)
        self._conn.commit()

    @property
    def close(self):
        # 关闭数据库连接
        self._conn.close()
        self.cur.close()
        db_info("数据库连接断开成功！")