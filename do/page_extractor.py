# -*- coding: utf-8 -*-
# 房源详情页数据提取
from .house_selector import HouseSelector
from module.downloader.page_extractor import PageExtratorDLD
from module.spider.page_extractor import PageExtractorSPR
from module.database.page_extractor import PageExtractorDB
from module.redis.page_extractor import PageExtractorRDS
from constant.value import PAGE_ID_COMPLIE
import re

class PageExtractor():

    @staticmethod
    def first_page_extract(size=20):
        '''第一次获取房源详情信息并入库
        - 失败的房源将被存入Redis中等待接下来的再次请求
        '''
        hs_iter = HouseSelector.id_list_iter(size)
        pe_rds = PageExtractorRDS()
        pe_db = PageExtractorDB()

        for house_id_list in hs_iter:
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
                    
                    # 未知错误
                    except Exception:
                        print("错误的房源编号", house_id)
                        raise