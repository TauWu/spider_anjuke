# SPIDER_ANJUKE

## 基本信息
ProjectName | Author | CreateDate | ChineseName
--- | --- | --- | ---
spider_anjuke | TauWoo | 2018-03-29 | 安居客房源信息爬虫

## 依赖模块
```sh
# 软件依赖
apt-get install python3
apt-get install python3-pip
apt-get install redis-server
apt-get install mysql-server
apt-get install python-bs4

# Python库依赖
pip3 install requests
pip3 install PyMySQL
pip3 install configparser
pip3 install beautifulsoup4
pip3 install lxml
pip3 install gevent
pip3 install fake-useragent
pip3 install redis
```

## 实现思路
1. 房源嗅探器从安居客提供的地图房源API中不断读取房源列表（同样的请求返回值不一样，依次为思路）；
2. 将从API获取到的房源ID和房源部分信息存入Redis中，如果已经有该值就更新；
3. 执行一段时间后将Redis中缓存的房源信息存入数据库中；
4. 从Redis获取房源ID列表，通过房源ID获取房源详情页面并获取其中的有效数据；

## 爬虫系统功能模块
模块名 | 含义 | 功能介绍
--- | --- | ---
do | 调度器 | 控制爬虫系统的调度。如请求并发，失败收集等
module.downloader | 下载器 | 对目标网站链接发起匿名HTTP请求，并将数据传递给spider模块
module.spider | 解析器 | 将下载器的下载的网页数据或者Json数据进行解析
module.database | 数据库操作器 | 控制爬虫系统的数据库操作，主要是爬虫数据入库
module.redis | Redis操作器 | 控制爬虫系统的Redis操作，主要是爬虫数据的缓存和房源库的构建

## 本项目模块介绍
模块名 | 含义 | 功能介绍
--- | --- | ---
HouseSelector | 房源嗅探器 | 从接口获取房源列表信息
PageExtractor | 页面信息提取 | 抽取房源详情页面的数据信息

## 并发建议
1. `房源嗅探器`+`存入Redis` 为一个进程，带sleep执行爬虫任务；
2. `Redis->DB`+`Redis->bs->DB` 为一个进程，此步骤较慢；

## 架构介绍
![image](https://raw.githubusercontent.com/TauWu/spider_anjuke/master/constant/images/spider_anjuke_workflow.png)
#### 架构图解说明
- 1.除了PriceStater，其他程序均为每日运行。PriceStater的运行周期是月
- 2.cba的意思是community/block/area，均是价格趋势图所需要的参数并且可以在HouseSelector中获取到
- 3.db1中的标记枚举如下：

value | 含义 
--- | ---
-1 | 没有运行过页面解析器
0 | 运行完成，中间没有发生任何错误
1 | 因网络原因导致的页面返回数据为空（目前已解决）
2 | 网页格局超出解析器工作范围的房源忽略（待解决）
