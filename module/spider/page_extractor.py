# -*- coding: utf-8 -*-
# 页面信息提取器

from bs4 import BeautifulSoup
import requests

class PageExtractorSPR():
    '''房源详情页面信息获取'''
    
    def __init__(self, page_text):
        self.soup = BeautifulSoup(page_text, "lxml")

    