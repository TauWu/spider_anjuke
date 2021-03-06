#!/usr/bin/python3.5
# -*- coding:utf-8 -*-
# 预运行工具 - 数据库操作工具

from util.database import DBController
from util.common.date import Time, DateTime
from util.config import ConfigReader
from util.common.logger import use_logger
from util.redis import RedisController

import sys
import time
import datetime

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
[4] 清空Redis。
[5] 刷新爬虫数量。

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

count_backup_sql = """

    INSERT INTO
        count_{tablename}
        ({columnname}, rows)
    SELECT 
        v.{columnname}, t.c
    FROM
        v_{tablename}_count as v
    INNER JOIN
        (
            SELECT 
                COUNT(1) AS c
            FROM
                {counttablename}
        ) AS t ON v.{columnname} = '{runtime}'
    ON DUPLICATE KEY 
        UPDATE {columnname}=v.{columnname}, rows=t.c

"""

def create(db):
    '''新建空表操作'''
    c1_sql = create_house_list_table.format(tablename=house_list_name)
    db.execute(c1_sql)
    
    ps_mday = ConfigReader.read_section_key("quota", "ps_mday")
    if int(ps_mday) == int(time.localtime().tm_mday):
        c2_sql = create_price_trend_table.format(tablename=price_trend_name)
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
    count_b1_sql = count_backup_sql.format(tablename=house_list_name,counttablename=house_list_name, columnname="run_date", runtime=t)
    db.execute(count_b1_sql)
    db.execute(b1_sql)

    ps_mday = ConfigReader.read_section_key("quota", "ps_mday")
    if int(ps_mday) == int(time.localtime().tm_mday):
        b2_sql = rename_sql.format(fromname=price_trend_name,toname="%s_%s"%(price_trend_name, t[:-2]))
        count_b2_sql = count_backup_sql.format(tablename=price_trend_name,counttablename=price_trend_name, columnname="run_month", runtime=t[:-2])
        db.execute(count_b2_sql)
        db.execute(b2_sql)

    create(db)
    truncate_redis()

def truncate_redis():
    # 清空Redis - PageExtractor
    rds = RedisController(section_name="redis_pe")
    rds._redis_conn.flushdb()

def refresh_count_table():
    '''刷新所有表的数据量'''
    bak_datetime = DateTime(ConfigReader.read_section_key("backup","start_date"))
    now_datetime = DateTime(Time.ISO_date_str())
    month_list = list()

    for _ in range(0, now_datetime-bak_datetime+1):
        date_str = bak_datetime.date_str
        month_str = date_str[:-2]
        backup_count_table(bak_datetime.date_str, month_str in month_list)
        bak_datetime += 1
        month_list.append(month_str)


def backup_count_table(t, flag):
    '''备份统计表'''
    count_b1_sql = count_backup_sql.format(tablename=house_list_name,counttablename="%s_%s"%(house_list_name, t), columnname="run_date", runtime=t)
    count_b2_sql = count_backup_sql.format(tablename=price_trend_name,counttablename="%s_%s"%(price_trend_name, t[:-2]),columnname="run_month", runtime=t[:-2])
    ps_mday = ConfigReader.read_section_key("quota", "ps_mday")

    try:
        db.execute(count_b1_sql)
        db_optor_info("【%s】房源日常备份成功！"%t)

    except Exception:
        db_optor_info("【%s】房源日常备份失败！"%(t))
    
    try:
        if not flag:
            db.execute(count_b2_sql)
            db_optor_info("【-%s-】价格趋势备份成功！"%(t[:-2]))
    except Exception:
        db_optor_info("【-%s-】价格趋势备份失败！"%(t[:-2]))

def opeartion(operator):
    '''操作提取函数'''
    operator = opeartor.strip()

    if operator == "0":
        raise UserWarning("程序退出...")

    elif opeartor == "1":
        db_optor_info("开始备份数据表...")
        backup_table(db, t)
        db_optor_info("备份完成！")

    elif opeartor == "2":
        db_optor_info("开始清空该数据表...")
        truncate(db)
        db_optor_info("清空完成！")

    elif opeartor == "3":
        db_optor_info("开始创建新的数据表...")
        create(db)
        db_optor_info("创建完成！")

    elif opeartor == "4":
        db_optor_info("开始清空Redis...")
        truncate_redis()
        db_optor_info("清空完成！")

    elif opeartor == "5":
        db_optor_info("开始刷新爬虫数量信息...")
        refresh_count_table()
        db_optor_info("刷新完成！")

    else:
        raise ValueError("【%s】操作不存在"%(opeartor))


if __name__ == "__main__":
    # 创建数据库连接
    db = DBController()
    # 获取当前时间
    t = Time.now_date_str()

    # 不携带参数的情况下交互式数据库操作
    if len(sys.argv) == 1:

        while True:

            opeartor = input(welcome_str)
            try:
                opeartion(opeartor)
            except UserWarning:
                break
            except ValueError as e:
                db_optor_info("请重新输入参数！%s"%str(e))
                continue

    # 携带一个参数的情况下直接执行一次该操作 - 为定时任务开发
    elif len(sys.argv) == 2:

        opeartor = sys.argv[1]

        try:
            opeartion(opeartor)
        except UserWarning:
            db_optor_info("没有任何操作")
        except ValueError as e:
            db_optor_info("没有任何操作 Err：%s"%str(e))
    
    else:
        raise ValueError("参数太多")

    db.close
