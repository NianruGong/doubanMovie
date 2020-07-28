# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# 采集对象类，一个电影信息就是一个类对象
class DoubanmovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 采集项，作为采集对象类的属性存在
    rank = scrapy.Field() # 电影的排名
    title = scrapy.Field() # 电影的名称
    star = scrapy.Field() # 评分
    link = scrapy.Field() # 详情连接
    img_url = scrapy.Field() # 海报图片
    pass
