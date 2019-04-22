# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

############对随机User_Agent 和 从代理IP池文件中随机获取IP进行请求进行封装#################

# DOWNLOADER_MIDDLEWARES = {

#    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':None,  
#    'bilibili.middlewares.ProxyMiddleWare':125,  
#    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': None,
     
#    'bilibili.middlewares.RandomUserAgentMiddleware': 543,
#    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None, #这里要设置原来的scrapy的useragent为None，否者会被覆盖掉
# }
# RANDOM_UA_TYPE = 'random'


# 放入middlewares.py文件内,并在settings.py中启用,同时设置 RANDOM_UA_TYPE = 'random' 配置
from fake_useragent import UserAgent  # 这是一个随机UserAgent的包，里面有很多UserAgent
from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware

class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()

        self.ua = UserAgent()
        self.ua_type = crawler.settings.get(
            'RANDOM_UA_TYPE', 'random')  # 从setting文件中读取RANDOM_UA_TYPE值

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            '''Gets random UA based on the type setting (random, firefox…)'''
            return getattr(self.ua, self.ua_type)

        user_agent_random = get_ua()
        # 这样就是实现了User-Agent的随即变换
        request.headers.setdefault('User-Agent', user_agent_random)

#——————————————————————————————————————————————————————————————————————————————————#
# 放入middlewares.py文件内,并在settings.py中启用,同时设置 RANDOM_UA_TYPE = 'random' 配置
 
from scrapy import log  
import time
import random
# logger = logging.getLogger()  

class ProxyMiddleWare(object):  
    """docstring for ProxyMiddleWare"""  
    def process_request(self,request, spider):  
        '''对request对象加上proxy'''  
        proxy = self.get_random_proxy()  
        print("当前请求的代理IP:"+proxy)  
        request.meta['proxy'] = proxy   


    def process_response(self, request, response, spider):  
        '''对返回的response处理'''  
        # 如果返回的response状态不是200，重新生成当前request对象  
        if response.status != 200:  
            proxy = self.get_random_proxy()  
            print("代理IP请求响应状态码不是200,自动更换代理IP重新请求,新的代理IP："+proxy)  
            # 对当前reque加上代理  
            request.meta['proxy'] = proxy   
            return request  
        return response  

    def get_random_proxy(self):  
        '''随机从文件中读取proxy'''  
        while 1:  
            with open('/Users/liyao/Desktop/GitCode/IP.txt',"r") as f:  
                proxies = f.readlines()  
            if proxies:  
                break  
            else: 
                time.sleep(1)  
        proxy = str(random.choice(proxies))
        return proxy  


################################## 默认middlewares.py #######################################


from scrapy import signals

class BilibiliSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BilibiliDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)










