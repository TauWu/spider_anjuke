# -*- coding: utf-8 -*-
# 房源价格趋势接口抓取数据库操作

from util.database import DBController
from constant.logger import db_err, db_info
from json import dumps

class PriceStaterDB():

    __name__ = "PriceStaterDB"

    @staticmethod
    def sql_creator(price_trend_json):
        sql = '''
        update
            anjuke_list
        set
            price_trend_json = '{price_trend_json}'\
        where
            house_id = {house_id}
        '''.format(
            house_id=price_trend_json["house_id"],
            price_trend_json=price_trend_json["data"]
        )
        return sql

    def __init__(self):
        self.db = DBController()

    @property
    def select_cba_key_iter(self):
        '''cba means community/block/area in database struct
        注意 本SQL中已经过滤掉可能重复的cba_key
        '''
        sql = """
        select 
            distinct(concat(community_id, '-', block_id, '-', area)) 
        from
            anjuke_list
        """
        self.db.execute(sql)
        data = self.db.cur.fetchall()
        data = [d[0] for d in data]
        for cba in data:
            yield tuple(cba.split('-'))

    def insert(self, json_data):
        '''向数据表中插入json_data
        (接口返回数据, 接口参数)
        '''
        sql_data = json_data[-1].split('-')
        sql_data.append(json_data[0])
        sql = """
        insert into
            anjuke_price_trend
            (`community_id`, `block_id`, `area_id`, `price_trend_json`)
        value
            (%s, %s, %s, '%s')
        """%(tuple(sql_data))
        try:
            self.db.execute(sql)
        except self.db.IntegrityError:
            db_info("忽略已存在的数据（%s %s %s）"%tuple(json_data[-1].split('-')))
        else:
            db_info("插入一条数据（%s %s %s）"%tuple(json_data[-1].split('-')))
            
    @property
    def exit(self):
        self.close
