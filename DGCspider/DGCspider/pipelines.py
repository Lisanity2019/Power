# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

# class DgcspiderPipeline(object):
            
#     def process_item(self, item, spider):
        
#         return item

class ImagesrenamePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for imgurl in item['image_urls']:
            yield Request(imgurl,meta={'name':str(item['model_name'])+'/'+str(item['img_name'])})
            
            
    #图片重命名
    def file_path(self, request, response=None, info=None):
        
        image_guid = request.url.split('/')[-1]
        name = request.meta['name']
        
        filename = u'{0}/{1}'.format(name, image_guid)
        
        # print("**************************    下载成功，文件名：" + filename + "   **************************")
        return filename

    
    


