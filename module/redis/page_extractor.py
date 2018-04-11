# -*- coding:utf-8 -*-
# 页面提取器Redis模块

from util.redis import RedisController

class PageExtractorRDS(RedisController):

    def __init__(self):
        self.rds = RedisController(db=1)    # 相对于房源库，选用另一个数据库

    def __insert_id__(self, house_id, err_type):
        '''插入房源ID的基础方法
        err_type枚举:
        - 0 请求成功，删除错误标记
        - 1 请求详情页面成功，但是页面返回为空值 
        - 2 页面由于加载不完全出现的部分元素信息缺失
        
        '''
        if err_type == 0:
            self.rds.rdel(house_id)
        else:
            self.rds.rset(house_id, err_type)

    def insert_empty_id(self, house_id):
        '''存放请求详情页面但页面返回数据为空的情况的房源ID'''
        self.__insert_id__(house_id, err_type=1)

    def insert_lose_element_id(self, house_id):
        '''存放页面加载不完全损失元素的房源ID'''
        self.__insert_id__(house_id, err_type=2)