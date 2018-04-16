# -*- coding: utf-8 -*-

from redis import Redis, ConnectionPool
import json
from util.config import ConfigReader
from constant.logger import *

class RedisController():
        
    def __init__(self, section_name="redis_hs"):
        (host, port, self.db) = ConfigReader.read_section_keylist(section_name, ["host","port","db"])
        self.__pool__ = ConnectionPool(host=host, port=port, db=self.db)
        self._redis_conn = Redis(connection_pool=self.__pool__)
        base_info("Redis连接%s创建成功！[%s:%s db%s]"%(section_name, host, port, self.db))

    def rset(self, key, value):
        self._redis_conn.set(key, value)
        redis_info("db%d:插入【%s => %s】"%(self.db, key, value))
    
    def rget(self, key):
        return self._redis_conn.get(key).decode('utf-8')

    def rdel(self, key):
        self._redis_conn.delete(key)
        redis_info("db%d:删除【%s】的缓存"%(self.db,key))

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