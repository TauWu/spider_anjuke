# -*- coding: utf-8 -*-
# 房源基础信息插入模块

from util.database import DBController
from constant.logger import *

def sql_creator(house_info):
    sql = '''
    insert into anjuke_list
        (
            house_id, rhval, community_id, community_name,
            rent_type_name, region_id, region_name, block_id,
            block_name, fitment, price, orient, is_list,
            broker_id, area, source_type, is_auction
        )
    values
        (
            {house_id}, '{rhval}', {community_id}, '{community_name}',
            '{rent_type_name}', {region_id}, '{region_name}', {block_id},
            '{block_name}', '{fitment}', {price}, '{orient}', {is_list},
            {broker_id}, {area}, {source_type}, {is_auction}
        )
    '''.format(house_id=house_info["id"], rhval=house_info["rhval"], community_id=house_info["community_id"],
            community_name=house_info["community_name"],rent_type_name=house_info["rent_type_name"],
            region_id=house_info["region_id"], region_name=house_info["region_name"], block_id=house_info["block_id"],
            block_name=house_info["block_name"], fitment=house_info["fitment"], price=house_info["price"], 
            orient=house_info["orient"], is_list=house_info["is_list"], broker_id=house_info["broker_id"],
            area=house_info["area"], source_type=house_info["source_type"], is_auction=house_info["is_auction"])
    return sql

class HouseSelectorDB(DBController):

    def __init__(self):
        self.db = DBController()
        
    def insert(self, house_info):
        self.house_info = house_info

        sql = sql_creator(self.house_info)
        try:
            self.db.execute(sql)
        except self.db.IntegrityError:
            db_warning("重复插入数据[%d]"%self.house_info["id"])
        except Exception:
            db_err("插入数据错误！[%d] %s"%(self.house_info['id'], sql))
        else:
            db_info("成功插入数据[%d]"%self.house_info["id"])

