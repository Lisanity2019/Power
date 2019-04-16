# -*- coding: utf-8 -*-
import scrapy
from DGCspider.items import DgcspiderItem


class DgcSpider(scrapy.Spider):
    name = 'dgc'
    # allowed_domains = ['www.meitulu.com']
    my_url = "https://www.meitulu.com/t/yanni/"
    start_urls = [my_url]
    temp_url_list = [my_url]
    temp_url_second_list = []
    i = 0
    j = 0

    def parse(self, response):
        # 根据姓名分类获取所有图集url地址
        base_url = response.xpath("//ul[@class='img']/li/a/@href").extract()
        for img_index_url in base_url:
            self.temp_url_second_list.append(img_index_url)

            yield scrapy.Request(img_index_url, callback=self.parse_index)
        # 如果有多页，就提取其他页url地址

        base_nextpage_url = response.xpath(
            "//div[@id='pages']/a[4]/@href").extract()[0]
        if (base_nextpage_url != self.temp_url_list[self.i]):
            self.i += 1
            self.temp_url_list.append(base_nextpage_url)
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
        baseurl = "https://www.meitulu.com"
        next_page = baseurl + next_page_tmp

        if (next_page != self.temp_url_second_list[self.j]):
            self.i += 1
            self.temp_url_second_list.append(next_page)
            print("^^^^^^^^^^^^^^^^^^^^^^^^"+response.urljoin(next_page_tmp)+"^^^^^^^^^^^^^^^^^^^^^^^^")
            yield scrapy.Request(next_page, callback=self.parse_index)
