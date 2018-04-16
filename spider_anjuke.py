# -*- coding: utf8 -*-

from do.house_selector import HouseSelector
from do.page_extractor import PageExtractor

if __name__ == "__main__":
    HouseSelector.spider_to_rds()
    HouseSelector.rds_to_db()
    PageExtractor.first_page_extract(50)