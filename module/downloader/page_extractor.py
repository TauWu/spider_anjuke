# -*- coding: utf-8 -*-
# 页面信息筛选器下载器

from util.web.proxies import ProxiesRequests
from constant.value import AJKPageURL, headers

class PageExtratorDLD(ProxiesRequests):
    '''页面信息筛选器下载器'''

    def __init__(self, house_id_list):
        self.url_list = [AJKPageURL.format(house_id=house_id) for house_id in house_id_list]
        self.__downloader__

    @property
    def __downloader__(self):
        ProxiesRequests.__init__(self, self.url_list)
        self.add_headers(headers=headers)
        res = self.req_content_list
        self.res = [(rec[0].decode("utf-8"), rec[1]) for rec in res]