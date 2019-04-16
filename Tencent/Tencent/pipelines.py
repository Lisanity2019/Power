# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class MyEncoder(json.JSONEncoder):
 
    def default(self, obj):
        """
        只要检查到了是bytes类型的数据就把它转为str类型
        :param obj:
        :return:
        """
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)

class TencentPipeline(object):
    def __init__(self):
        self.f = open("tencent.json", "w")

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False,cls=MyEncoder)+",\n"
        self.f.write(content)
        return item

    def close_spider(self, spider):
        self.f.close()
