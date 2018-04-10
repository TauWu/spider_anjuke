# -*- coding: utf-8 -*-
# 房源筛选器入Redis模块

from util.redis import RedisController

class HouseSelectorRDS(RedisController):
    def __init__(self):
        self.rds = RedisController()

    def insert(self, house_id, house_info):
        self.rds.rset(house_id, house_info)
    
    def select(self, size):
        return self.rds.rscan(size)