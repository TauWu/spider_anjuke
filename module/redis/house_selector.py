# -*- coding: utf-8 -*-
# 房源筛选器入Redis模块

from util.redis import RedisController

class HouseSelectorRDS(RedisController):

    @staticmethod
    def insert(house_id, house_info):
        rds = RedisController()
        rds.rset(house_id, house_info)