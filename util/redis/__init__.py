# -*- coding: utf-8 -*-

from redis import Redis, ConnectionPool
import json
from .config import host, port, db
from ..common.logger import base_info, use_logger

@use_logger(level="info")
def redis_info(msg):
    pass

class RedisController():

    def __init__(self, db=db):
        self.__pool__ = ConnectionPool(host=host, port=port, db=db)
        self._redis_conn = Redis(connection_pool=self.__pool__)
        base_info("Redis连接创建成功！")

    def rset(self, key, value):
        self._redis_conn.set(key, value)
        redis_info("db%d:插入【%s => %s】"%(db, key, value))
    
    def rget(self, key):        
        return self._redis_conn.get(key).decode('utf-8')

    def rdel(self, key):
        self._redis_conn.delete(key)
        redis_info("db%d:删除【%s】的缓存"%(db,key))

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

    @property
    def rscan(self):
        '''扫描Redis'''
        for key in self._redis_conn.keys():
            yield key.decode('utf-8'), self.rget(key).replace("\'","\"")

if __name__ == "__main__":
    pass