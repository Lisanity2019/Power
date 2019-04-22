# -*- coding: utf-8 -*-
import scrapy
from DGCspider.items import DgcspiderItem


class DgcSpider(scrapy.Spider):
    name = 'dgc'
    # allowed_domains = ['www.meitulu.com']
    my_url = "https://www.meitulu.com/t/1273/"
    start_urls = [my_url]

  

    def parse(self, response):
        # 根据姓名分类获取所有图集url地址
        base_url = response.xpath("//ul[@class='img']/li/a/@href").extract()
        for img_index_url in base_url:
            yield scrapy.Request(img_index_url, callback=self.parse_index)

        # 当前图集如果有多页，就提取其他页url地址，发送请求
        base_nextpage_url = response.xpath(
            "//div[@id='pages']/a[4]/@href").extract()[0]
        if (base_nextpage_url):
            scrapy.Request(base_nextpage_url, callback=self.parse)

    def parse_index(self, response):
        # 每页img链接列表
        img_list = response.xpath(
            "//div[@class='content']/center/img/@src").extract()
        temp_img_name = response.xpath(
            "//div[@class='c_l']/p[2]/text()").extract()[0]
        model_name = response.xpath("//div[@class='c_l']/p[5]/a[1]/text()").extract()[0]
         
        img_name = temp_img_name.split('：')[-1]

        for image_urls in img_list:
            item = DgcspiderItem()
            item['image_urls'] = [image_urls]
            item['img_name'] = [img_name]
            item['model_name']=[model_name]
            yield item

        # 循环爬取下一页
        next_page_tmp = response.xpath(
            "//div[@id='pages']/a[last()]/@href").extract()[0]
        if(next_page_tmp):
            # 拼接绝对路径
            next_page_url = response.urljoin(next_page_tmp)
            yield scrapy.Request(next_page_url, callback=self.parse_index)  # 默认已去重        
