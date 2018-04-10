# SPIDER_ANJUKE

## 基本信息
ProjectName | Author | CreateDate | ChineseName
--- | --- | --- | ---
spider_anjuke | TauWoo | 2018-03-29 | 安居客房源信息爬虫

## 实现思路
1. 房源嗅探器从安居客提供的地图房源API中不断读取房源列表（同样的请求返回值不一样，依次为思路）；
2. 将从API获取到的房源ID和房源部分信息存入Redis中，如果已经有该值就更新；
3. 执行一段时间后将Redis中缓存的房源信息存入数据库中；
4. 从Redis获取房源ID列表，通过房源ID获取房源详情页面并获取其中的有效数据（暂定用scrapy）；

## 并发建议
1. `房源嗅探器`+`存入Redis` 为一个进程，带sleep执行爬虫任务；
2. `Redis->DB`+`Redis->scrapy->DB` 为一个进程，此步骤较慢；
3. `Timer（待确认）`为一个进程，主要计时是否需要继续运行第一个进程。