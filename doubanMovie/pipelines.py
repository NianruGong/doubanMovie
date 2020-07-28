# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#import importlib
#import sys

#default_encoding = 'utf-8'

#if sys.getdefaultencoding()!=default_encoding:
#    importlib.reload(sys)
#    sys.setdefaultencoding(default_encoding)

# useful for handling different item types with a single interface
import csv
import json
import os
import re
from scrapy import Request
from pymysql import connect
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


# 保存为json文件
from scrapy.utils.project import get_project_settings


class jsonPipeline(object):
    def process_item(self, item, spider):
        file_path=os.getcwd()+'\\dataResult\\'+'doubanMovie.json'
        with open(file_path,'a+',encoding='utf-8') as fp:
            line = json.dumps(dict(item),ensure_ascii=False)+"\n"
            fp.write(line)
            return item

# 保存为excel文件
class xlsPipeline(object):
    def process_item(self, item, spider):
        file_path = os.getcwd() + '\\dataResult\\'+'doubanMovie.csv'
        with open(file_path, 'a+',encoding='utf-8-sig',newline='') as fp:
            if os.path.getsize(file_path)==0:
               csv.writer(fp,dialect="excel").writerow(('电影排名','电影名称','电影评分','标记人数','详情连接','电影海报'))
               csv.writer(fp,dialect="excel").writerow((item['rank'],item['title'],item['star'][0],item['star'][1],item['link'],item['img_url']))
            else:
               csv.writer(fp,dialect="excel").writerow((item['rank'],item['title'],item['star'][0],item['star'][1],item['link'],item['img_url']))
            return item

# 保存到mysql
class mysqlPipeline(object):
    def __init__(self):
        self.connect = connect(host='localhost',
                               db='test',
                               user='root',
                               passwd='123456',
                               charset='utf8',
                               use_unicode=True)
        # 连接数据库
        self.cursor = self.connect.cursor()
        # 使用cursor()方法获取操作游标

    def process_item(self, item, spider):
        self.cursor.execute("insert into movietop250 values(%s,%s,%s,%s,%s,%s)",
                            (item['rank'],
                             item['title'],
                             item['star'][0],
                             item['star'][1],
                             item['link'],
                             item['img_url']
                             ))
        # 执行sql语句，item里面定义的字段和表字段一一对应
        self.connect.commit()
        # 提交
        return item
        # 返回item

    def close_spider(self, spider):
        self.cursor.close()
        # 关闭游标
        self.connect.close()
        # 关闭数据库连接

# 下载海报图片
class imagePipeline(ImagesPipeline):
    IMAGES_STORE = get_project_settings().get("IMAGES_STORE")

    def get_media_requests(self, item, info):
        for image_url in item['img_url']:
            yield Request(image_url, meta={'img_name': item['title']})

    def file_path(self, request, response=None, info=None):
        image_name = request.meta['img_name'] # 通过上面的meta传递过来item'
        return 'movieimg/%s.jpg'%(image_name)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if image_path:
            return item
        else:
            raise DropItem('image download failed')

class DoubanmoviePipeline(object):
    def process_item(self, item, spider):
        print('电影排名：{0}'.format(item['rank'][0]))
        print('电影名称：{0}'.format(item['title'][0]))
        print('电影评分：{0}'.format(item['star'][0]))
        print('评分人数：{0}'.format(item['star'][1]))
        print('详情连接：{0}'.format(item['link'][0]))
        print('海报图片：{0}'.format(item['img_url'][0]))
        print('-'*20)
        return item
