# 这里存放的是代理测试代码

# 本处代理使用的是 http://www.xdaili.cn/

import time
import hashlib
import requests
import re

# 多线程 + 协程
from multiprocessing import Process
import gevent
from gevent import monkey; monkey.patch_all()

# 异步HTTP请求
import aiohttp
import asyncio

# 配置文件
from config import *

# 代理 用户验证部分 - 一天检查一次，所以多次调用时不重复此步骤
timestamp = str(int(time.time()))
string = "orderno={orderno},secret={secret},timestamp={timestamp}".format(orderno=orderno,secret=secret,timestamp=timestamp)
string=string.encode()
md5_string = hashlib.md5(string).hexdigest()
sign = md5_string.upper()
auth = "sign=%s&orderno=%s&timestamp=%s"%(sign, orderno, timestamp)

# requests代理设置
proxy = {"http": "http://%s"%ip_port, "https": "https://%s"%ip_port}
headers = {"Proxy-Authorization": auth}

def fetch(url, num):
    while True:
        try:
            # URL请求发送
            r = requests.get(url, headers=headers, proxies=proxy, verify=False, allow_redirects=False, timeout=2)
            # 正常页面请求输出
            text = r.content.decode("gb2312")
            ip_info = re.findall(r"<center>您的IP是：\[(.+)\] 来自：(.+)</center>", text)
            if len(ip_info) == 0:
                # 端口转发频率太频繁，重新发起请求
                continue
            print(ip_info, num)
            break
        except Exception:
            print("请求超时编号%d，正在重新发起"%num)
            # 请求超时重新发起新的请求
            continue

def process_start(tasks):
    gevent.joinall(tasks)

def task_start():
    task_list = []
    for i in range(0, 5):
        task_list.append(gevent.spawn(fetch, raw_url, i))
    # process_start(task_list)
    for i in range(0,3):
        p = Process(target=process_start, args=(task_list, ))
        p.start()

async def get(url, num):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(url, i)
            print(url, i, await resp.text())

loop = asyncio.get_event_loop()

tasks = []
for i in range(0, 20):
    tasks.append(get(raw_url, i))

loop.run_until_complete(asyncio.wait(tasks))
loop.close()