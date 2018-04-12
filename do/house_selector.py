# -*- coding: utf-8 -*-
# 房源嗅探器

from do import *
import json

class HouseSelector():
    '''此处存放房源嗅探器的操作'''

    @staticmethod
    def spider_to_rds(times=10, size=50):
        '''从接口获取房源ID列表并存入Redis'''
        hs = HouseSelectorSPR(times, size)
        hs_rds = HouseSelectorRDS()

        house_infos = hs.house_id_list
        for house_info in house_infos:
            hs_rds.insert(house_info["id"], house_info)

    @staticmethod
    def rds_to_db():
        '''将Redis中的房源信息存入DB'''
        hs_rds = HouseSelectorRDS()
        hs_db = HouseSelectorDB()

        hs_data_iter = hs_rds.select()
        for hs_data in hs_data_iter:
            try:
                hs_db.insert(json.loads(hs_data[1]))
            except Exception as e:
                db_err("Redis数据插入数据库错误 %s"%(str(e)))
        
        hs_db.db.close

    @staticmethod
    def id_list_iter(size=20):
        '''获取一个房源ID列表的迭代器'''
        hs_rds = HouseSelectorRDS()
        hs_data_iter = hs_rds.select()

        while True:
            house_id_list = list()
            for _ in range(0, size):
                try:
                    hs_data = next(hs_data_iter)
                except Exception:
                    break
                else:
                    house_id_list.append(hs_data[0])
            if len(house_id_list) == 0:
                break
            yield house_id_list