#!/usr/bin/python3.5
#!/usr/bin/python3
# -*- coding: utf-8 -*-

from util.config import ConfigParser

def default_config(key, value):
    return key

def get_config():
    
    # 数据库配置
    print("开始配置数据库...")
    db_host = input("请输入数据库的host（跳过为localhost）")
    db_user = input("请输入数据库的user（跳过为root）")
    db_port = input("请输入数据库的端口（跳过为3306）")
    db_pwd = input("请输入数据库的pwd（跳过为root）")
    db_db = input("请输入数据库的数据库名（跳过为spider_anjuke）")

    if len(db_host) == 0:
        db_host = "127.0.0.1"
    if len(db_user) == 0:
        db_user = "root"
    if len(db_pwd) == 0:
        db_pwd = "root"
    if len(db_db) == 0:
        db_db = "spider_anjuke"
    if len(db_port) == 0:
        db_port = "3306"
    
    # 代理配置
    while True:
        print("开始配置代理相关信息...")
        proxy_order_no = input("请输入代理订单号码")
        proxy_secret = input("请输入代理secret密钥")
        proxy_ip_port = "forward.xdaili.cn:80"
        proxy_raw_url = "http://2017.ip138.com/ic.asp"

        if len(proxy_order_no) == 0 or len(proxy_secret) == 0:
            print("【发现非法空值】orderno或secret为空，请填写正确的值！")
            continue
        else:
            break
        
    # Redis配置
    # BasicInfo Redis
    print("开始配置Redis连接...")
    redis_host = input("请输入Redis的host（跳过为localhost）")
    if len(redis_host) == 0:
        redis_host = "127.0.0.1"
    redis_port = input("请输入Redis端口号（跳过为6379）")
    if len(redis_port) == 0:
        redis_port = "6379"
    redis_port = int(redis_port)
            
    # HouseSelector Redis
    redis_hs_db = input("请输入HS的Redis数据库编号（数字）")
    redis_hs_db = int(redis_hs_db)
            
    # PageExtractor Redis
    redis_pe_db = input("请输入PE的Redis数据库编号（数字）")
    redis_pe_db = int(redis_pe_db)
            
    # PriceStater Redis
    redis_ps_db = input("请输入PS的Redis数据库编号（数字）")
    redis_ps_db = int(redis_ps_db)

    # 配额配置
    print("开始配置爬虫配额...")
    hs_times = input("请输入HouseSelector执行的次数（跳过为10次）")
    if len(hs_times) == 0:
        hs_times = 10
    hs_size = input("请输入HouseSelector每次嗅探的链接并发量（跳过为50）")
    if len(hs_size) == 0:
        hs_size = 10    

    pe_times = input("请输入PageExtractor循环步骤中执行的次数（跳过为5次）")
    if len(pe_times) == 0:
        pe_times = 10
    pe_size = input("请输入PageExtractor每次的链接并发量（跳过为20次）")
    if len(pe_size) == 0:
        pe_size = 10
        
    ps_mday = input("请输入PriceStater每次运行于几号（跳过为1号）")
    if len(ps_mday) == 0:
        ps_mday = 10
    ps_size = input("请输入PriceStater每次链接请求的并发量（跳过为20次）")
    if len(ps_size) == 0:
        ps_size = 10
                    
    return dict(
        database=dict(host=db_host, user=db_user, passwd=db_pwd, db=db_db, port=db_port),
        proxy = dict(orderno=proxy_order_no, secret=proxy_secret, 
            ip_port=proxy_ip_port, raw_url=proxy_raw_url),
        redis_hs = dict(host=redis_host, port=redis_port, db=redis_hs_db),
        redis_pe = dict(host=redis_host, port=redis_port, db=redis_pe_db),
        redis_ps = dict(host=redis_host, port=redis_port, db=redis_ps_db),
        quota = dict(hs_times=hs_times, hs_size=hs_size, pe_times=pe_times, 
            pe_size=pe_size, ps_mday=ps_mday, ps_size=ps_size)
    )
    
if __name__ == "__main__":
    # 配置文件基础
    cp = ConfigParser(config_file="spider.cfg")
    config_dict = get_config()

    # 填写配置文件
    for k in config_dict.keys():
        cp.add_section(k)
        for k_inner in config_dict[k]:
            cp.set_kv(k_inner, config_dict[k][k_inner])