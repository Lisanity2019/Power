# -*- coding: utf-8 -*-
import scrapy
import json
from bilibili.items import BilibiliItem
import re


# 分析：
# 1.当前用户的关注列表接口 https://api.bilibili.com/x/relation/followers?vmid={mid}&pn=1&ps=20&order=desc&jsonp=jsonp&callback   mid为用户的唯一ID标识  拿到mid 以及当前用户的关注总数’total‘ 利用’total‘去遍历构造获取每一页请求地址，得到当前用户的所有粉丝的mid，然后对每个关注的mid重复执行第一步 ##调试发现，只能正常访问粉丝列表的前5页

# 2.用拿到的mid构造该用户的信息 接口 https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp


class BiliuserSpider(scrapy.Spider):
    name = 'biliuser'
    # allowed_domains = ['www.bilibili.com']
    start_urls = [
        'https://api.bilibili.com/x/relation/followings?vmid=37974444&pn=1&ps=20&order=desc&jsonp=jsonp&callback']
    parse_url_template = 'https://api.bilibili.com/x/relation/followings?{}&pn={}&ps=20&order=desc&jsonp=jsonp&callback'
    follow_url_template = 'https://api.bilibili.com/x/relation/followings?vmid={}&pn=1&ps=20&order=desc&jsonp=jsonp&callback'
    userinfo_url_template = 'https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp'


    def parse(self, response):
        '''
        遍历当前用户关注mid的所有页面url，调用parse_ollow方法进一步处理
        '''
        resultJson_parse = json.loads(response.body)
        total = resultJson_parse['data']['total']
        # print(response.request.url)  #当前响应的url地址
        response_url = response.request.url
        str_mid = re.findall('vmid=\d*', response_url)[0]

        if (total <= 20):
            yield scrapy.Request(self.parse_url_template.format(str_mid, 1), callback=self.parse_follow)
        elif (20 < total <= 100 and (total % 20 != 0)):
            for i in range(1, (total // 20) + 2):
                yield scrapy.Request(self.parse_url_template.format(str_mid, i), callback=self.parse_follow)
        elif (20 < total <= 100 and (total % 20 == 0)):
            for i in range(1, (total // 20) + 1):
                yield scrapy.Request(self.parse_url_template.format(str_mid, i), callback=self.parse_follow)
        else:
            for i in range(1, 6):
                yield scrapy.Request(self.parse_url_template.format(str_mid, i), callback=self.parse_follow)

    def parse_follow(self, response):
        '''
        获取当前用户所关注用户的mid 并回调parse_userinfo方法对该用户的个人信息抓取
        '''
        resultJson_follow = json.loads(response.body)
        follow_user_list = resultJson_follow['data']['list']

        for follow_user in follow_user_list:
            mid = follow_user['mid']
            # 回调parse方法对每个mid的关注用户进行爬取
            yield scrapy.Request(self.follow_url_template.format(mid), callback=self.parse)
            yield scrapy.Request(self.userinfo_url_template.format(mid), callback=self.parse_userinfo)

    def parse_userinfo(self, response):
        '''
        爬取用户的mid name sex信息
        '''
        userinfo_resultJson = json.loads(response.body)
        userinfo_result = userinfo_resultJson['data']
        item = BilibiliItem()
        item['_id'] = userinfo_result['mid']
        item['name'] = userinfo_result['name']
        item['level'] = userinfo_result['level']
        item['coins'] = userinfo_result['coins']
        item['sex'] = userinfo_result['sex']
        yield item
