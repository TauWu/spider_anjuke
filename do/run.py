# -*- coding: utf-8 -*-
# 总调度器 + 多线程控制器
from do.house_selector import HouseSelector
from do.page_extractor import PageExtractor
from do.price_stater import PriceStater

from util.config import ConfigReader
from constant.logger import *

import time

class Do(HouseSelector, PageExtractor, PriceStater):

    @staticmethod
    def step_hs(times=10, size=50):
        '''程序第一步'''
        base_info("开始运行HouseSelector times=%d size=%d"%(times, size))
        HouseSelector.spider_to_rds(times=times, size=size)
        HouseSelector.rds_to_db()
    
    @staticmethod
    def step_pe(times=5, size=20):
        '''程序第二步'''
        base_info("开始运行PageExtractor times=%d size=%d"%(times, size))
        PageExtractor.base_page_extract(size=size)
        PageExtractor.loop_page_extract(size=size, times=times)

    @staticmethod
    def step_ps(size=20, mday=1):
        '''程序第三步 - 价格趋势表每月获取一次'''
        if mday == int(time.localtime().tm_mday):
            base_info("开始运行PriceStater size=%d, mday=%d"%(size, mday))
            PriceStater.price_stat(size=size)
        else:
            base_info("今天不是%d号，不执行PriceStater"%mday)
    
    @staticmethod
    def do(use_normal=True):
        '''默认运行方法
        - use_normal:使用默认值执行程序
        '''
        from multiprocessing import Process

        if use_normal:
            hs_times = 10
            hs_size  = 50
            pe_times = 5
            pe_size  = 20
            ps_mday  = 1
            ps_size  = 20
        else:
            cfg_reader = ConfigReader(config_file="spider.cfg", section_name="quota")
            hs_times = cfg_reader.read("hs_times")
            hs_size  = cfg_reader.read("hs_size")
            pe_times = cfg_reader.read("pe_times")
            pe_size  = cfg_reader.read("pe_size")
            ps_mday  = cfg_reader.read("ps_mday")
            ps_size  = cfg_reader.read("ps_size")
        
        Do.step_hs(times=int(hs_times), size=int(hs_size))

        p_step_pe = Process(target=Do.step_pe, args=(int(pe_times), int(pe_size), ))
        p_step_ps = Process(target=Do.step_pe, args=(int(ps_size), int(ps_mday), ))

        p_step_pe.start()
        p_step_ps.start()


            