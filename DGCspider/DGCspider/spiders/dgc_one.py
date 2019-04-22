# -*- coding: utf-8 -*-
import scrapy
from DGCspider.items import DgcspiderItem

# 适用于没有model目录的单个抓取


class DgcOneSpider(scrapy.Spider):
    name = 'dgc_one'
    # allowed_domains = ['w']
    myurl = "https://www.meitulu.com/item/17095.html"
    start_urls = [myurl]

    def parse(self, response):
        # 每页img链接列表
        img_list = response.xpath(
            "//div[@class='content']/center/img/@src").extract()
        temp_img_name = response.xpath(
            "//div[@class='c_l']/p[2]/text()").extract()[0]
        model_name_tmp = response.xpath(
            "//div[@class='c_l']/p[5]/text()").extract()[0]
        model_name = model_name_tmp.split('：')[-1]

        img_name = temp_img_name.split('：')[-1]

        for image_urls in img_list:
            item = DgcspiderItem()
            item['image_urls'] = [image_urls]
            item['img_name'] = [img_name]
            item['model_name'] = [model_name]
            yield item

        # 循环爬取下一页
        next_page_tmp = response.xpath(
            "//div[@id='pages']/a[last()]/@href").extract()[0]
        if(next_page_tmp):
        # 拼接绝对路径
            next_page_url = response.urljoin(next_page_tmp)
            yield scrapy.Request(next_page_url, callback=self.parse)  # 默认已去重
