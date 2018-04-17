# -*- coding: utf-8 -*-
# 价格趋势获取器

from util.web.proxies import ProxiesRequests
from module.database.price_stater import PriceStaterDB
from constant.value import *
from constant.logger import *
import random
import json

class PriceStaterSPR(ProxiesRequests, PriceStaterDB):

    def __init__(self, size=50):
        '''价格趋势获取器
        '''
        self.size = size
        self.current_url_list = list()
        PriceStaterDB.__init__(self)
        self.cba_key_iter = self.select_cba_key_iter
        self.flag = 0

    @property
    def __get_url_list__(self):
        self.current_url_list = list()
        try:
            for _ in range(0, self.size):
                cba = next(self.cba_key_iter)
                self.current_url_list.append(PRICE_TREND_URL%cba)
        except StopIteration:
            self.flag += 1
            return False
        else:
            return True
    
    @staticmethod
    def single_mutil_req(url_list):
        '''单次并发请求并返回值'''
        
        pr = ProxiesRequests(url_list)
        pr.add_headers(headers=headers)
        
        res = pr.req_content_list
        
        for rec in res:
            rec = (json.dumps(json.loads(rec[0].decode("unicode_escape"))["data"]).encode("utf-8").decode("unicode_escape"), "-".join(list(re.findall(CBA_ID_COMPILE,rec[1])[0])))
            yield rec
        
    @property
    def price_stat_json_iter(self):
        while True:
            flag = self.__get_url_list__
            if flag or self.flag <= 1:
                yield from PriceStaterSPR.single_mutil_req(self.current_url_list)
            else:
                break