# -*- coding: utf-8 -*-

from module.spider.price_stater import PriceStaterSPR
from module.database.price_stater import PriceStaterDB

class PriceStater():

    @staticmethod
    def price_stat(size=20):
        ps_spr = PriceStaterSPR(size)
        ps_db = PriceStaterDB()
        json_iter = ps_spr.price_stat_json_iter
        for j in json_iter:
            ps_db.insert(j)
        ps_db.exit
