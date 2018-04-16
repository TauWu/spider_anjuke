# -*- coding: utf-8 -*-
# 页面信息提取器

from bs4 import BeautifulSoup
import requests, re

from constant.value import SUBMIT_DATE_COMPILE

class PageExtractorSPR():
    '''房源详情页面信息获取'''
    
    def __init__(self, page_text):
        self.soup = BeautifulSoup(page_text, "lxml")
        self.__get_page_info__

    @property
    def __get_page_info__(self):
        soup = self.soup

        # 详情页标题
        title = soup.select_one("body > div.wrapper > h3").get_text()
        
        # 详情页Tag
        price, rooms, halls, area = [text.get_text() for text in soup.findChild("div",{"class":"title-basic-info clearfix"}).findChildren("em")]
        rent_type, orientation, subway = [text.get_text() for text in soup.findChild("ul",{"class":"title-label cf"}).findChildren("li")]
        subway = subway[:-2].split("/")
        tag = dict(price=price, rooms=rooms, halls=halls, area=area, rent_type=rent_type, orientation=orientation, subway=subway)
        
        # 发布时间
        submit_date = re.findall(SUBMIT_DATE_COMPILE, soup.findChild("div", {"class":"right-info"}).get_text())[0]

        # 详情页房屋信息
        price = soup.select_one("body > div.wrapper > div.mainbox.cf > div.lbox > ul.house-info-zufang.cf > li.full-line.cf > span.price").get_text()
        payment = soup.select_one("body > div.wrapper > div.mainbox.cf > div.lbox > ul.house-info-zufang.cf > li.full-line.cf > span.type").get_text()
        house_info = [text.get_text() for text in soup.findChild("ul", {"class":"house-info-zufang cf"}).findChildren("span",{"class":"info"})]
        house_type, area, orientation, floor, level, house_level = house_info[:6]
        gender = str()
        if len(house_info) == 7:
            gender = house_info[-1]
        
        community_info = re.findall(r'([\u4e00-\u9fa5]+)', str(soup.findChild("ul",{"class":"house-info-zufang cf"}).findChildren("li",{"class":"house-info-item l-width"})[-1]))

        if len(community_info) == 4:
            community, district, busi_area = community_info[1:]
        elif len(community_info) == 5:
            community, _, district, busi_area = community_info[1:]
        else:
            print(community_info)
            a = input("DEBUG")
            
        house_info = dict(price=price, payment=payment, house_type=house_type, area=area, floor=floor, orientation=orientation, level=level,\
        house_level=house_level, gender=gender, community=community, district=district, busi_area=busi_area)
        
        self.house_page_info = dict(title=title, tag=tag, submit_date=submit_date, house_info=house_info)