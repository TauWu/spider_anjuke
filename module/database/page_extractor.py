# -*- coding: utf-8 -*-
# 房源详情页抓取器数据库操作

from util.database import DBController
from constant.logger import *
from json import dumps

class PageExtractorDB():

    __name__ = "PageExtractorDB"

    @staticmethod
    def sql_creator(page_info):
        sql = '''
        update
            anjuke_list
        set
            page_info_json = '{page_info_json}'
        where
            house_id = {house_id}
        '''.format(
            page_info_json=dumps(page_info["data"]).encode('utf-8').decode('unicode_escape'), 
            house_id=page_info["house_id"] 
        )
        return sql

    def __init__(self):
        self.db = DBController()

    def update(self, page_info):
        sql = PageExtractorDB.sql_creator(page_info)

        try:
            self.db.execute(sql)
        except Exception:
            db_err("[%s]插入数据错误[%s] %s"%(self.__name__, page_info['house_id'], sql))
        else:
            db_info("[%s]成功插入数据[%s]"%(self.__name__, page_info["house_id"]))

