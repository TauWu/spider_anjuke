# -*- coding: utf-8 -*-
# 价格趋势获取Redis部分

from util.redis import RedisController

class PriceStaterRDS(RedisController):

    def __init__(self):
        self.rds = RedisController(section_name="redis_ps")

    def __insert_id__(self, cba_id, err_type):
        '''插入cbaid的基础方法
        err_type枚举：
        - 0 请求成功
        - 1 json返回为空值（当前已在请求基础方法中封堵）
        - 2 json返回无法被解析
            
        '''
        self.rds.rset(cba_id, err_type)

    def select(self):
        return self.rds.rscan

    def insert_success_id(self, cba_id):
        '''插入成功的cba'''
        self.__insert_id__(cba_id, err_type=0)
    
    def insert_empty_id(self, cba_id):
        '''插入返回空值的cba'''
        self.__insert_id__(cba_id, err_type=1)

    def insert_unloadable_id(self, cba_id):
        '''插入成功的cba'''
        self.__insert_id__(cba_id, err_type=2)