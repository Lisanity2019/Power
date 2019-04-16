from scrapy.cmdline import execute
import os
import sys

#此文件放入与scrapy.cfg同级文件目录里,以py脚本方式启动爬虫

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy','crawl','爬虫文件名'])