# -*- coding: utf-8 -*-
# 房源嗅探器 从地图接口中不断尝试获取房源列表

from util.web.proxies import ProxiesRequests
from constant.value import *
from constant.logger import *
import random
import json

class HouseSelectorSPR(ProxiesRequests):

    def __init__(self, times=10, size=50):
        '''房源嗅探器 从地图接口中不断尝试获取房源列表
        入参：
            times: 嗅探次数
            size: 并发数量
        '''
        self.times = times
        self.size = size + 1
        self.current_url_list = list()

    @property
    def __get_url_list__(self):
        '''获取指定size的待请求的URL列表'''
        for idx in range(0, self.size):
            self.current_url_list.append(RAW_URL.format(page=random.randint(1,100)))

    @property
    def __clean_url_list__(self):
        '''清空url_list中的待请求链接'''
        self.current_url_list = list()

    @property
    def __single_mutil_req__(self):
        '''单次并发请求并返回值'''
        self.__get_url_list__
        
        ProxiesRequests.__init__(self, self.current_url_list)
        self.add_headers(headers=headers)
        res = self.req_content_list
        for rec in res:
            try:
                rec = json.loads(rec[0].decode("unicode_escape"))["val"]["props"]
            except Exception:
                continue
            else:
                yield rec
                
        self.__clean_url_list__
                    
    @property
    def house_id_list(self):
        '''获取房源ID列表'''
        for i in range(0, self.times):
            res = self.__single_mutil_req__
            for house_infos in res:
                for house_info in house_infos:
                    yield house_info