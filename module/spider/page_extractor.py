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
        title = soup.select_one("body > div.wrapper > h3").get_text().strip()
        
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
        
        community_info = [re.findall(r'>(.+)</a>', str(i))[0] for i in soup.findChild("ul",{"class":"house-info-zufang cf"}).\
            findChildren("li",{"class":"house-info-item l-width"})[-1].findChildren("a",{"_soj":"propview"})]

        if len(community_info) == 3:
            community, district, busi_area = community_info[:]
        elif len(community_info) == 2:
            district, busi_area = community_info[:]
            community = re.findall(r'</span>([\s\S]+)\(<a',str(soup.findChild("ul",{"class":"house-info-zufang cf"}).\
                findChildren("li",{"class":"house-info-item l-width"})[-1]))[0].replace("\t","").replace(" ","").replace('\n','')
            raise RuntimeWarning("房源信息重新解析 %s %s %s"%(district, busi_area, community))
        else:
            raise ValueError("房源信息解析错误 %s"%str(community_info))
            
        house_info = dict(price=price, payment=payment, house_type=house_type, area=area, floor=floor, orientation=orientation, level=level,\
        house_level=house_level, gender=gender, community=community, district=district, busi_area=busi_area)
        
        self.house_page_info = dict(title=title, tag=tag, submit_date=submit_date, house_info=house_info)