# -*- coding: utf-8 -*-

from redis import Redis, ConnectionPool
from .config import host, port
from ..common.logger import base_info, use_logger

@use_logger(level="info")
def redis_info(msg):
    pass

class RedisController():

    def __init__(self):
        self.__pool__ = ConnectionPool(host=host, port=port)
        self._redis_conn = Redis(connection_pool=self.__pool__)
        base_info("Redis连接成功！")

    def rset(self, key, value):
        self._redis_conn.set(key, value)
        redis_info("插入【%s】－【%s】"%(key, value))
    
    def rget(self, key):
        return str(self._redis_conn.get(key))[2:-1]

    def rdel(self, key):
        self._redis_conn.delete(key)
        redis_info("删除key为【%s】的缓存"%key)

    @property
    def dbsize(self):
        return self._redis_conn.dbsize()

    def rpipeset(self, lists):

        pipe = self._redis_conn.pipeline(transaction=True)

        for list_detail in lists:
            key = list(list_detail.keys())[0]
            value = list_detail[key]
            self.rset(key, value)
        
        pipe.execute()

if __name__ == "__main__":
    r = RedisController()
    r.rset("1","SH0003407698")

    lists = list()
    list_detail = dict()
    for i in range(2,5):
        list_detail[str(i)] = "SH0003407714"
        lists.append(list_detail)
        list_detail = dict()
    
    print(lists)

    r.rpipeset(lists)