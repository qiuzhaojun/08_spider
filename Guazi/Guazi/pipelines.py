# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# 管道1功能: 终端打印输出汽车名
class GuaziPipeline(object):
    def process_item(self, item, spider):
        print('pipelines:', item['name'])

        return item

# 管道2功能: 数据存入MySQL数据库
import pymysql
class GuaziMysqlPipeline(object):
    def open_spider(self, spider):
        """项目启动时,只执行一次,一般用于数据库连接"""
        self.db = pymysql.connect(
            'localhost', 'root', '123456',
            'cardb', charset='utf8'
        )
        self.cur = self.db.cursor()
        self.ins = 'insert into cartab values(%s,%s,%s)'
        print('天王盖地虎')

    def process_item(self, item, spider):
        li = [
            item['name'],
            item['price'],
            item['link'],
        ]
        self.cur.execute(self.ins, li)
        self.db.commit()

        return item

    def close_spider(self, spider):
        """项目结束时,只执行一次,一般用于数据库断开"""
        self.cur.close()
        self.db.close()
        print('宝塔镇河妖')

# 管道3功能: 数据存入MongoDB数据库
import pymongo
class GuaziMongoPipeline(object):
    def open_spider(self, spider):
        self.conn = pymongo.MongoClient(
            'localhost', 27017
        )
        self.db = self.conn['cardb']
        self.myset = self.db['carset']

    def process_item(self, item, spider):
        self.myset.insert_one(dict(item))

        return item




