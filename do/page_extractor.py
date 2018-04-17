# -*- coding: utf-8 -*-
# 房源详情页数据提取
from .house_selector import HouseSelector
from module.downloader.page_extractor import PageExtratorDLD
from module.spider.page_extractor import PageExtractorSPR
from module.database.page_extractor import PageExtractorDB
from module.redis.page_extractor import PageExtractorRDS

from constant.value import PAGE_ID_COMPLIE
from util.common.id_iter import house_id_iter
from constant.logger import *

import re

class PageExtractor():
    
    @staticmethod
    def id_list_iter(size=20):
        '''获取一个房源列表迭代器'''
        pe_rds = PageExtractorRDS()
        pe_data_iter = pe_rds.select()

        yield from house_id_iter(pe_data_iter, size)

    @staticmethod
    def base_page_extract(size=20):
        '''第一次获取房源详情信息并入库
        - 失败的房源将被存入Redis中等待接下来的再次请求
        '''
        pe_iter = PageExtractor.id_list_iter(size)
        pe_rds = PageExtractorRDS()
        pe_db = PageExtractorDB()

        for house_id_list in pe_iter:
            pe_downloader = PageExtratorDLD(house_id_list)
            for rec in pe_downloader.res:
                house_id = re.findall(PAGE_ID_COMPLIE,rec[1])[0]
                if len(rec[0]) == 0:
                    '''详情页面在请求完成后没有返回数据 错误代码：1'''
                    pe_rds.insert_empty_id(house_id)
                else:
                    try:
                        pe_spr = PageExtractorSPR(rec[0])
                        page_info = dict(data=pe_spr.house_page_info, house_id=house_id)
                        pe_db.update(page_info)
                        
                    # get_text函数报错
                    except AttributeError:
                        pe_rds.insert_lose_element_id(house_id)
                    
                    # 房源小区名称获取错误(算成功 需要人工检查)
                    except RuntimeWarning as w:
                        base_warn("警告房源编号%s 警告信息%s"%(house_id, str(w)))
                        pe_rds.insert_success_id(house_id)

                    # 未知错误
                    except Exception as e:
                        base_err("错误的房源编号%s 错误信息:%s"%(house_id, str(e)))
                    else:
                        pe_rds.insert_success_id(house_id)

    @staticmethod
    def loop_page_extract(size=20):
        '''循环获取页面信息直到...
        - 直到的条件待定
        '''
        pass