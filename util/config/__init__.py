# -*- coding:utf-8 -*-
# 配置文件基础模块

import configparser

class ConfigParser():

    def __init__(self, config_file='config.cfg', section_name='config'):
        self.config_file = config_file
        self.section_name = section_name
        self.config = configparser.ConfigParser()

    def add_section(self, section_name):
        self.config.add_section(section_name)
        self.use_section(section_name)

    def use_section(self, section_name):
        self.section_name = section_name

    def set_kv(self, k, v):
        self.config.set(self.section_name, k, str(v))
        self.save

    def read(self, k):
        self.config.read(self.config_file)
        return self.config[self.section_name][k]

    @property
    def save(self):
        self.config.write(open(self.config_file, 'w'))

class ConfigReader(ConfigParser):

    @staticmethod
    def read_section_key(section_name, k):
        cp = ConfigParser(config_file='spider.cfg', section_name=section_name)
        return cp.read(k)

    @staticmethod
    def read_section_keylist(section_name, k_list):
        v_list = list()
        for k in k_list:
            v_list.append(ConfigReader.read_section_key(section_name=section_name, k=k))
        return tuple(v_list)