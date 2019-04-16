# -*- coding: utf-8 -*-
import json

import scrapy

from douban.items import DoubanItem


class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanmovie'
    # allowed_domains = ['douban']
    start_urls = [
        'https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0']
    url_template = "https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start={}"

    for offset in range(20, 500, 20):
        start_urls.append(url_template.format(offset))

    def parse(self, response):
        resultJson = json.loads(response.body)
        subjects = resultJson['subjects']
        for subject in subjects:
            item = DoubanItem()
            item['score'] = subject['rate']
            item['title'] = subject['title']
            item['url'] = subject['url']
            yield item

        pass
