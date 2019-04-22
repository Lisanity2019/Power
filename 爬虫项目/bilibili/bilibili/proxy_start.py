# -*- coding: UTF-8 -*-
'''
Python 3.x

描述：本段代码定时从API接口获取代理IP，存入IP池中

'''
import requests
import time
import threading

from requests.packages import urllib3

# 获取代理IP的线程类
class GetIpThread(threading.Thread):
    def __init__(self,apiUrl, fetchSecond):
        super(GetIpThread, self).__init__()
        self.fetchSecond=fetchSecond
        self.apiUrl=apiUrl
    def run(self):
        while True:
            # 获取IP列表
            res = requests.get(self.apiUrl).content.decode()
            # 按照\n分割获取到的IP
            
            IPPOOL = res.split('\n')
            
            with open('IP.txt',"a") as f:
                for proxyip in IPPOOL:
                    if (proxyip and len(proxyip)<22):
                        f.write("http://"+proxyip+'\n')
                
            # 休眠
            time.sleep(self.fetchSecond)


# if __name__ == "__main__":

#     # 获取IP的API接口
# apiUrl = "http://webapi.http.zhimacangku.com/getip?num=20&type=1&pro=&city=0&yys=0&port=1&pack=50220&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions="  #免费API
# apiUrl = "http://d.jghttp.golangapi.com/getip?num=50&type=1&pro=&city=0&yys=0&port=1&pack=8770&ts=0&ys=0&cs=0&lb=4&sb=0&pb=4&mr=1&regions="  #免费API
apiUrl = "http://http.tiqu.qingjuhe.cn/getip?num=20&type=1&pro=&city=0&yys=0&port=1&pack=30092&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=0&regions="  #免费API
    # 获取IP时间间隔，建议为5秒
fetchSecond = 300
    # 开始自动获取IP
GetIpThread(apiUrl, fetchSecond).start()



