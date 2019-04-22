# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import pymongo
from scrapy import Item

class BilibiliPipeline(object):
    '''
    将item写入MongoDB数据库
    '''

    @classmethod
    def from_crawler(cls, crawler):
        cls.DB_URL = crawler.settings.get('MONGO_DB_URL', 'mongodb://localhost:27017')
        cls.DB_NAME = crawler.settings.get('MONGO_DB_NAME', 'bilibili_data')
        return cls()
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.DB_URL)
        self.db = self.client[self.DB_NAME]
        
    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        post = dict(item) if isinstance(item, Item) else item
        collection.insert_one(post)
        print("当前时间:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        print("*"*8,"用户ID：",item['_id'],"    写入数据库成功","*"*8)
        
        return item

from scrapy.exceptions import DropItem

class DropDataPipeline(object):
    '''
    mid去重
    '''
    def __init__(self):
        self.ids_seen = set()
    def process_item(self, item, spider):
        if item['_id'] in self.ids_seen:
            raise DropItem("mid已经存在: %s" % item)
        else:
            self.ids_seen.add(item['_id'])
            return item


