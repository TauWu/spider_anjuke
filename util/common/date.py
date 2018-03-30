# -*- coding: utf-8 -*-

import time

class Time(object):

    def __init__(self):
        pass

    @staticmethod
    def now_date_str():
        '''返回形如20180301的日期字符串'''
        return time.strftime("%Y%m%d", time.localtime())

    @staticmethod
    def now_time_str():
        '''返回形如120102的时间字符串'''
        return time.strftime("%H%M%S", time.localtime())

    @staticmethod
    def now_str():
        '''返回形如20180101_120102的时间字符串'''
        return time.strftime("%Y%m%d_%H%M%S", time.localtime())

    @staticmethod
    def now_datetime_str():
        '''返回形如20180101_120102的时间字符串'''
        return Time.now_str()

    @staticmethod
    def ISO_str():
        '''返回标准时间字符串 2018-12-12 12:13:14'''
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @staticmethod
    def ISO_datetime_str():
        '''返回标准时间字符串 2018-12-12 12:13:14'''
        return Time.ISO_str()

    @staticmethod
    def ISO_date_str():
        '''返回标准日期字符串 2018-12-12'''
        return time.strftime("%Y-%m-%d", time.localtime())

    @staticmethod
    def ISO_time_str():
        '''返回标准时间字符串12:13:14'''
        return time.strftime("%H:%M:%S", time.localtime())

if __name__ == "__main__":
    print (Time.now_date_str())
    print (Time.now_datetime_str())