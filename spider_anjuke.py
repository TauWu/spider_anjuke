# -*- coding: utf8 -*-

from util.database import DBController
import requests
import time
import json

headers = {
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
}

RAW_URL = "https://sh.zu.anjuke.com/v3/ajax/recommend/?type=list&num=60&guid=1E7FFD54-71DC-0198-D017-8D4FA919E655&price_id=&price_lower=&price_upper=&list_type=area&area_id=7&other_id=&city_id=11"

def req():
    idx = 0
    while True:
        idx += 1
        print("*****************第%d次请求..."%idx)
        rec_list = []
        for rec in json.loads(requests.get(RAW_URL,allow_redirects=False,headers=headers).content.decode("unicode_escape"))["rec_list"]:
            yield rec

if __name__ == "__main__":
    db = DBController()
    r = req()
    while True:
        house = next(r)
        house_id, title = house["id"], "test"
        print(house_id, title)
        sql = "insert into anjuke_list(house_id, title) values({house_id}, '{title}')".format(house_id=house_id, title=title)
        try:
            db.execute(sql)
            db._conn.commit()
        except Exception as e:
            print(house_id,"ERR!",e)
        time.sleep(0.1)
    db.close