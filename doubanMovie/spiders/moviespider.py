import logging

import scrapy
from venv import logger
# 导入items中的DoubanmovieItem类
from doubanMovie.items import DoubanmovieItem

logger = logging.getLogger(__name__)

class MoviespiderSpider(scrapy.Spider):
    name = 'moviespider'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250'] # 将访问网页Url地址填写在start_urls列表中

    # 编写 parse( ) 函数的关键技术是XPath解析HTML标签，从而获取到对应的采集项数值
    def parse(self, response):
        # 获取当前页面中所有的电影采集标签item
        movie_items = response.xpath('//div[@class="item"]')
        # 使用for循环遍历每一个电影标签，获取采集数据项并封装成一个采集项对象
        for item in movie_items:
            print(type(item))
            # 创建一个空的DoubanmovieItem对象 电影采集类对象
            movie = DoubanmovieItem()
            # Xpath解析获取电影排名并为movie对象的rank属性赋值
            movie['rank'] = item.xpath('div[@class="pic"]/em/text()').extract()
            # Xpath解析获取电影排名并为movie对象的title属性赋值
            movie['title'] = item.xpath('div[@class="info"]/div[@class="hd"]/a/span[@class="title"][1]/text()').extract()
            # 电影评分 参与评分人数
            movie['star'] = item.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span/text()').extract()
            # 电影详情连接
            movie['link'] = item.xpath('div[@class="pic"]/a/@href').extract()
            # 海报图片
            movie['img_url'] = item.xpath('div[@class="pic"]/a/img/@src').extract()
            # 将添加好的movie添加到一个生成器中
            yield movie
        pass

        # 取下一页的地址
        nextPageURL = response.xpath('//span[@class="next"]/a/@href').extract()
        # print(nextPageURL)
        if nextPageURL:
            url = response.urljoin(nextPageURL[-1])
            # print('url', url)
            # 发送下一页请求并调用parse()函数继续解析
            yield scrapy.Request(url, self.parse, dont_filter=False)
            pass
        else:
            print("退出")

        logger.warning('日志信息')

        pass
