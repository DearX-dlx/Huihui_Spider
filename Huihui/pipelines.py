# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

#导入系统设计，也就是刚刚我们设计的全局变量
from scrapy.conf import settings
#导入异常处理机制
from scrapy.exceptions import DropItem
#log功能
from scrapy import log

class HuihuiPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipeline(object):
    #初始化方法
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        #链接数据库
        db = connection[settings['MONGODB_DB']]
        if not db:
            print '数据库连接失败'
        #(表)
        self.collection = db[settings['MONGODB_COLLECTION']]
        if not self.collection:
            print 'collection获取失败'

    #链接数据库的通道
    def process_item(self, item, spider):

        valid = True
        for data in item:
            if not data:
                raise DropItem("数据库通道未接收到数据")
        #把数据录入数据库
        self.collection.insert(dict(item))
        log.msg("successful add!!!",level=log.DEBUG,spider=spider)

        return item
