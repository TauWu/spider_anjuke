# -*- coding: utf-8 -*-
# 房源详情页抓取器数据库操作

from util.database import DBController
from constant.logger import db_err, db_info
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
        except Exception as e:
            db_err("[%s]更新数据错误[%s] %s %s "%(self.__name__, page_info['house_id'], str(e), sql))
        else:
            db_info("[%s]成功更新数据[%s]"%(self.__name__, page_info["house_id"]))
