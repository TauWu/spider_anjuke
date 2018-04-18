#!/usr/bin/python3.5
# -*- coding:utf-8 -*-
# 预运行工具 - 数据库操作工具

from util.database import DBController
from util.common.date import Time
import sys

from util.common.logger import use_logger

@use_logger(level="info")
def db_optor_info(msg):
    pass

# 这里存放可能会有操作的SQL语句模板
house_list_name = "anjuke_list"
price_trend_name = "anjuke_price_trend"

welcome_str = """
请输入您需要进行的操作的数字编号：
---
[0] 退出。
[1] 备份当前数据表为当前时间，并创建新的空数据表。
[2] 清空当前数据表。
[3] 新建数据表。

---

"""

truncate_sql = "truncate table `{tablename}`"
rename_sql = "rename table `{fromname}` to `{toname}`"

create_house_list_table = """
    CREATE TABLE IF NOT EXISTS `{tablename}` (

    `house_id` int(11) NOT NULL COMMENT '房源编号',
    `title` varchar(127) DEFAULT '' COMMENT '房源标题',
    `rhval` varchar(15) DEFAULT '' COMMENT '户型',
    `community_id` int(15) COMMENT '地标ID',
    `community_name` varchar(63) DEFAULT '' COMMENT '地标名称',
    `rent_type_name` varchar(15) DEFAULT '' COMMENT '出租类型',
    `region_id` int(15) COMMENT '行政区ID',
    `region_name` varchar(15) DEFAULT '' COMMENT '行政区名称',
    `block_id` int(15) COMMENT '商圈ID',
    `block_name` varchar(15) COMMENT '商圈名称',
    `fitment` varchar(15) COMMENT '装修情况',
    `price` int(11) COMMENT '房间标价',
    `orient` varchar(15) COMMENT '房间朝向',
    
    `is_list` int(4) COMMENT '未知字段1',
    `broker_id` int(15) COMMENT '未知字段2',
    `area` int(15) COMMENT '未知字段3',
    `source_type` int(15) COMMENT '未知字段4',
    `is_auction` int(4) COMMENT '未知字段5',

    `page_info_json` json COMMENT '房源详情页面JSON',
    
    `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最近修改时间',
    `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`house_id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

"""

create_price_trend_table = """

    CREATE TABLE IF NOT EXISTS `{tablename}` (

    `community_id` int(15) COMMENT '地标ID',
    `block_id` int(15) COMMENT '商圈ID',
    `area_id` int(15) COMMENT '未知字段3',

    `price_trend_json` json COMMENT '价格趋势JSON',
    
    `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最近修改时间',
    `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`community_id`, `block_id`, `area_id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

"""

def create(db):
    '''新建空表操作'''
    c1_sql = create_house_list_table.format(tablename=house_list_name)
    c2_sql = create_price_trend_table.format(tablename=price_trend_name)

    db.execute(c1_sql)
    db.execute(c2_sql)


def truncate(db):
    '''清空缓存表操作'''
    t1_sql = truncate_sql.format(tablename=house_list_name)
    t2_sql = truncate_sql.format(tablename=price_trend_name)

    db.execute(t1_sql)
    db.execute(t2_sql)

def backup_table(db, t):
    '''备份缓存表操作'''
    b1_sql = rename_sql.format(fromname=house_list_name,toname="%s_%s"%(house_list_name, t))
    b2_sql = rename_sql.format(fromname=price_trend_name,toname="%s_%s"%(price_trend_name, t))

    db.execute(b1_sql)
    db.execute(b2_sql)

    create(db)

if __name__ == "__main__":
    # 创建数据库连接
    db = DBController()
    
    # 获取当前时间
    t = Time.now_date_str()

    # 不携带参数的情况下交互式数据库操作
    if len(sys.argv) == 1:

        while True:

            opeartor = input(welcome_str)

            if opeartor.strip() == "0":
                db_optor_info("程序退出...")
                break

            elif opeartor.strip() == "1":
                db_optor_info("开始备份数据表...")
                backup_table(db, t)
                db_optor_info("备份完成！")

            elif opeartor.strip() == "2":
                db_optor_info("开始清空该数据表...")
                truncate(db)
                db_optor_info("清空完成！")

            elif opeartor.strip() == "3":
                db_optor_info("开始创建新的数据表...")
                create(db)
                db_optor_info("创建完成！")

            else:
                db_optor_info("\n【%s】操作不存在，请重新选择！"%opeartor)
                continue

    # 携带一个参数的情况下直接执行一次该操作 - 为定时任务开发
    elif len(sys.argv) == 2:

        opeartor = sys.argv[1]

        if opeartor.strip() == "1":
            db_optor_info("开始备份数据表...")
            backup_table(db, t)
            db_optor_info("备份完成！")

        elif opeartor.strip() == "2":
            db_optor_info("开始清空该数据表...")
            truncate(db)
            db_optor_info("清空完成！")

        elif opeartor.strip() == "3":
            db_optor_info("开始创建新的数据表...")
            create(db)
            db_optor_info("创建完成！")
    
    else:
        raise ValueError("参数太多")

    db.close