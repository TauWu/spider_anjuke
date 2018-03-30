# 本处代理使用的是 http://www.xdaili.cn/

import time
import hashlib
import requests

# 多线程 + 协程
from multiprocessing import Process
import gevent
from gevent import monkey; monkey.patch_all()

# 配置文件
from .config import *
from ..common.logger import use_logger

@use_logger(level="warn")
def req_warn(msg):
    pass

@use_logger(level="err")
def req_err(msg):
    pass


# 代理 用户验证部分 - 一天检查一次，所以多次调用时不重复此步骤
class ProxiesHeaders():
    '''
    使用本代理 需要在请求头中添加Proxy-Authorization字段

    '''
    def __init__(self):
        self.__timestamp = str(int(time.time()))
        self.__string = "orderno={orderno},secret={secret},timestamp={timestamp}".format(orderno=orderno,secret=secret,timestamp=self.__timestamp)
        self.__string=self.__string.encode()

    @property
    def _auth_(self):
        self.__md5_string = hashlib.md5(self.__string).hexdigest()
        self.__sign = self.__md5_string.upper()
        self._auth = "sign=%s&orderno=%s&timestamp=%s"%(self.__sign, orderno, self.__timestamp)
        return self._auth

    @property
    def auth_with_time(self):
        # 搭配时间戳保证时间间隔为一天（第三方要求）
        auth = self._auth_
        timestamp = self.__timestamp
        return auth, timestamp

class ProxiesRequests(ProxiesHeaders):
    '''
    通过端口转发发起请求
    这里发起的请求应当是一个待请求的 列表

    '''
    def __init__(self, urls=[]):
        ProxiesHeaders.__init__(self)
        self._urls = urls
        self.__auth_with_time = self.auth_with_time
        self.__proxy_auth = self.__auth_with_time[0]
        self.__timestamp = self.__auth_with_time[1]
        self._proxy = {"http": "http://%s"%ip_port, "https": "https://%s"%ip_port}
        self._headers = {"Proxy-Authorization": self.__proxy_auth}
        self._single_content = None
        self._content = list()

    @property
    def _get_headers_(self):
        return self._headers

    def _proxy_request_(self, url):
        self._proxy_content_singal_(url)
        self._content.append((self._single_content, url))

    def _proxy_content_singal_(self, url):
        '''发起单个的代理请求 可被继承'''

        # 去除代理不安全的警告 - InsecureRequestWarning
        import requests
        from requests.packages.urllib3.exceptions import InsecureRequestWarning 
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        while True:
            try:
            # URL 请求发送
                req = requests.get(url, headers=self._headers, proxies=self._proxy, allow_redirects=False, timeout=2, verify=False)#
                req_content = req.content

                if str(req_content).find("The number of requests exceeds the limit") != -1 or str(req_content).find("Concurrent number exceeds limit") != -1:
                    # 端口转发太频繁 重新发起请求
                    time.sleep(0.5)
                    continue
                self._single_content = req_content
                break
            except Exception as e:
                req_warn("请求失败！正在重新发起... %s"%str(e))
                time.sleep(0.5)
                continue

    @property
    def _batch_request_(self):
        '''协程执行请求 可被继承'''
        task_list = []
        for url in self._urls:
            task_list.append(gevent.spawn(self._proxy_request_, url))
        gevent.joinall(task_list)

    @property
    def req_content_list(self):
        self._batch_request_
        return self._content

    def add_headers(self, headers):
        '''特殊的网页请求可以添加Headers'''
        self._headers = dict(self._headers, **headers)

    def add_cookies(self, cookies):
        '''特殊网页请求可以添加Cookies'''
        headers_tmp = {"Cookies":cookies}
        self.add_headers(headers_tmp)

class ProxiesVaild(ProxiesRequests):
    '''测试代理代码'''

    def __init__(self, num=1):
        self.vaild_urls = []
        self.ip_infos = []
        for i in range(0, num):
            self.vaild_urls.append(raw_url)
        ProxiesRequests.__init__(self, self.vaild_urls)
        
    def _get_ip_info_(self, content):
        '''从网页中获取IP信息'''
        import re

        ip_info = re.findall(r"<center>您的IP是：\[(.+)\] 来自：(.+)</center>", content)
        try:
            ip_info = ip_info[0]
            return ip_info
        except Exception as e:
            req_err("未有匹配 %s %s %s"%(str(e)," content: ", content))
            return

    @property
    def vaild_proxies_a(self):
        '''A验证 req打包发送 resp打包返回'''
        for url in self.vaild_urls:
            self._proxy_request_(url)
        for _single_content in self._content:
            self.ip_infos.append(self._get_ip_info_(_single_content[0].decode("gb2312")))
        return self.ip_infos

    @property
    def _vaild_proxies_b_base(self):
        '''请求分别发送 更省内存'''
        for url in self.vaild_urls:
            self._proxy_content_singal_(url)
            yield self._get_ip_info_(self._single_content.decode("gb2312"))

    @property
    def vaild_proxies_b(self):
        '''B验证 req打包发送 resp分别返回'''
        for ip_info in self._vaild_proxies_b_base:
            self.ip_infos.append(ip_info)
        return self.ip_infos

    def clear_ip_info(self):
        self.ip_infos = []