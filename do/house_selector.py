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
    def rds_to_db(size=200):
        '''将Redis中的房源信息存入DB'''
        hs_rds = HouseSelectorRDS()
        hs_db = HouseSelectorDB()

        hs_data_total = hs_rds.select(100)
        for hs_data in hs_data_total:
            for hs in hs_data:
                try:
                    hs_db.insert(json.loads(hs[1]))
                except Exception as e:
                    db_err("Redis数据插入数据库错误 %s"%(str(e)))
        
        hs_db.db.close
