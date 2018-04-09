# -*- coding: utf8 -*-

# from util.database import DBController
# from util.web.proxies import ProxiesRequests
# from util.common.logger import use_logger
# import requests
# import time
# import json
# import random
# from util.redis import RedisController

# def get_url_list(num):
#     url_list = list()
#     for i in range(0,num):
#         url_list.append(RAW_URL.format(page=random.randint(1,100)))
#     return url_list

# def req():
#     idx = 0
#     while True:
#         idx += 1
        
#         r = ProxiesRequests(get_url_list(50))
#         r.add_headers(headers=headers)

#         result_list = r.req_content_list

#         for result in result_list:
#             try:
#                 result = json.loads(result[0].decode("unicode_escape"))["val"]["props"]
#             except Exception:
#                 continue
#             else:
#                 for rec in result:
#                     yield rec

# if __name__ == "__main__":
#     db = DBController()
#     r = req()
#     while True:
#         house = next(r)
#         house_id, title = house["id"], "test"
#         sql = "insert into anjuke_list(house_id, title) values({house_id}, '{title}')".format(house_id=house_id, title=title)
#         try:
#             db.execute(sql)
#             db._conn.commit()
#         except Exception as e:
#             db_err("插入【%s】失败！"%(house_id))
#         else:
#             db_info("插入【%s】成功！"%(house_id))
#         # time.sleep(0.05)
#     db.close

from module.spider.house_selector import HouseSelector
from module.database.house_selector import HouseSelectorDB

if __name__ == "__main__":
    hs = HouseSelector(10,10)
    house_ids = hs.house_id_list
    for house_id in house_ids:
        HouseSelectorDB.insert(house_id)