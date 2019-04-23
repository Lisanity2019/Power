# 美图录的模特写真套图爬取
# 说明：
## 1.基于Scrapy爬虫框架
## 2.重写了ImagesPipeline类的def get_media_requests方法和file_path文件重命名方法
***
## 使用说明：
## 1.爬虫文件dgc实现了根据美图录模特分类索引爬取该模特所有图集，并按**模特名字/图集编号/图片文件**形式存储到本地。可在settings.py里修改本地保存路径`IMAGES_STORE = '/Volumes/文档/IMG/images'`
## 2.dgc爬虫传入模特的分类索引页url
## 3.dgc_one爬虫是对没有模特分类索引进行单个图集爬取，传入单个图集url
***