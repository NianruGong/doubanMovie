import pymysql
from scrapy import cmdline
from lazyspider.lazystore import LazyMysql
# 先创建mysql对应的table

def createDatabase():
    con = pymysql.connect(host='localhost', user='root',passwd='123456', charset='utf8')
    cur = con.cursor()
    #cur.execute("create database IF NOT EXISTS test character set utf8;")
    cur.execute("use test;")
    cur.execute("CREATE TABLE IF NOT EXISTS movietop250(rank char(10),\
                                                        title char(30),\
                                                        rating char(30),\
                                                        paticipants char(30),\
                                                        link char(255),\
                                                        img_url char(255))\
                                                        ENGINE=InnoDB DEFAULT CHARSET='utf8';")
    cur.close()
    # 关闭数据库连接
    con.close()

if __name__ == '__main__':
    createDatabase()
    cmdline.execute("scrapy crawl moviespider".split())