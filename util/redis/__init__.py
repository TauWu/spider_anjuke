# -*- coding: utf-8 -*-

from redis import Redis, ConnectionPool
import json
from util.config import ConfigReader
from constant.logger import *

def equal(object1, object2):
    obj1_type = type(object1)
    obj2_type = type(object2)

    # 判断类型
    if obj1_type != obj2_type:
        return False
    else:
        # 是json？
        if obj1_type == str:
            try:
                object1_json = json.loads(object1.replace("\'","\""))
                object2_json = json.loads(object2.replace("\'","\""))
            except Exception:
                pass
            else:
                if object1_json == object2_json:
                    return True
        else:
            if object1 == object2:
                return True
            else:
                return False


class RedisController():
        
    def __init__(self, section_name="redis_hs"):
        (host, port, self.db) = ConfigReader.read_section_keylist(section_name, ["host","port","db"])
        self.__pool__ = ConnectionPool(host=host, port=port, db=self.db)
        self._redis_conn = Redis(connection_pool=self.__pool__)
        base_info("Redis连接%s创建成功！[%s:%s db%s]"%(section_name, host, port, self.db))

    def rset(self, key, value):
        rvalue = self.rget(key)
        if equal(str(value), str(rvalue)):
            redis_info("db%s:set【%s => <=】"%(self.db, key))
        elif rvalue == None:
            redis_info("db%s:set【%s () => %s】"%(self.db, key, value))
        else:
            redis_info("db%s:set【%s %s => %s】"%(self.db, key, rvalue, value))
        self._redis_conn.set(key, value)
    
    def rget(self, key):
        try:
            res = self._redis_conn.get(key)
            if res is not None:
                return res.decode('utf-8')
            else:
                return None
        except Exception as e:
            print(str(e))
            return None

    def rdel(self, key):
        self._redis_conn.delete(key)
        redis_info("db%s:删除【%s】的缓存"%(self.db,key))

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