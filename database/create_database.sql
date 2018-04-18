CREATE DATABASE IF NOT EXISTS `spider_anjuke`;

USE `spider_anjuke`;

CREATE TABLE IF NOT EXISTS `anjuke_list` (

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

CREATE TABLE IF NOT EXISTS `anjuke_price_trend` (

  `community_id` int(15) COMMENT '地标ID',
  `block_id` int(15) COMMENT '商圈ID',
  `area_id` int(15) COMMENT '未知字段3',

  `price_trend_json` json COMMENT '价格趋势JSON',
  
  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最近修改时间',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`community_id`, `block_id`, `area_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
