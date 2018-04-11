# -*- coding: utf-8 -*-
# 房源详情页数据提取
from .house_selector import HouseSelector
from module.downloader.page_extractor import PageExtratorDLD
from module.spider.page_extractor import PageExtractorSPR
from module.redis.page_extractor import PageExtractorRDS
import re

class PageExtractor():

    @staticmethod
    def first_page_extract():
        '''第一次获取房源详情信息并入库
        - 失败的房源将被存入Redis中等待接下来的再次请求
        '''
        hs_iter = HouseSelector.id_list_iter(5)
        pe_rds = PageExtractorRDS()

        for house_id_list in hs_iter:
            pe_downloader = PageExtratorDLD(house_id_list)
            text_list = list()
            for rec in pe_downloader.res:
                if len(rec[0]) == 0:
                    '''详情页面在请求完成后没有返回数据 错误代码：1'''
                    pe_rds.insert_empty_id(re.findall(r"fangyuan/(.+)\?from=",rec[1])[0])
                else:
                    PageExtractorSPR(rec[0])
                    a = input("DEBUG")