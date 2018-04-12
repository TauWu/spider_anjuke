# -*- coding: utf8 -*-

from do.house_selector import HouseSelector
from do.page_extractor import PageExtractor

from util.config import ConfigParser

if __name__ == "__main__":
    cp = ConfigParser()
    cp.add_section("config")
    cp.set_kv("123", "321")
    cp.set_kv("sda","3123")
    cp.save
    print(cp.read("sda"))
    # HouseSelector.spider_to_rds()
    # HouseSelector.rds_to_db()
    # PageExtractor.first_page_extract(50)