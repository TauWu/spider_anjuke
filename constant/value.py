# 请求头常量
headers = {
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
}

# 链接常量
RAW_URL = "https://sh.zu.anjuke.com/v3/ajax/map/rent/3219/prop_list/?p={page}&maxp=99&room_num=0&price_id=0&rent_type=0&price_min=0&price_max=0&lx_id=&tag_id=&orient_id=&order_id=0&lat=31.064245_31.527833&lng=121.108875_121.833269&zoom=12&ib=1&et=d8eab6&bst=pzm190"
AJKPageURL = "https://sh.zu.anjuke.com/fangyuan/{house_id}?from=Filter_1&hfilter=filterlist"
PRICE_TREND_URL = "https://sh.zu.anjuke.com/v3/ajax/getPriceTrend?comm_id=%s&block_id=%s&area_id=%s&num=12"

# 正则匹配常量
import re

PAGE_ID_COMPLIE = re.compile(r"fangyuan/(.+)\?from=")
CBA_ID_COMPILE = re.compile(r'comm_id=([0-9]+)&block_id=([0-9]+)&area_id=([0-9]+)')
SUBMIT_DATE_COMPILE = re.compile(r"房屋编码：[0-9]+，发布时间：(.+)")