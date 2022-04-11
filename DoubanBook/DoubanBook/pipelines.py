# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter


class DoubanbookPipeline(object):
    def process_item(self, item, spider):
        print(dict(item))
        return item

class mysqlPipeline(object):
    def open_spider(self,spider):
        "爬虫项目只启动一次，用于数据库连接"
        self.db = pymysql.Connect(
            host= 'localhost',
            user= 'root',
            password= '123456',
            database= 'douban_book'
        )

        self.cursor = self.db.cursor()

    def process_item(self,item,spider):
        """处理从爬虫文件传过来的item数据"""
        ins = "insert into book(name) values(%s)"
        name_list = item['name']
        self.cursor.execute(ins,name_list)
        self.db.commit()
        return item

    def close_spider(self,spider):
        """爬虫程序结束时只执行1次,一般用于数据库断开"""
        self.cursor.close()
        self.db.close()