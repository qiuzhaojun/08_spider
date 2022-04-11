"""
链家二手房数据抓取
"""
import requests
from lxml import etree
from fake_useragent import UserAgent
import time
import random
import pymongo

class LianjiaSpider:
    def __init__(self):
        self.url = 'https://bj.lianjia.com/ershoufang/pg{}/'
        # 3个对象
        self.conn = pymongo.MongoClient(
            'localhost', 27017
        )
        self.db = self.conn['lianjiadb']
        self.myset = self.db['lianjiaset']

    def get_html(self, url):
        headers = {'User-Agent':UserAgent().random}
        html = requests.get(url=url,
                            headers=headers).content.decode('utf-8', 'ignore')
        # 直接调用解析函数
        self.parse_html(html)

    def parse_html(self, html):
        """解析函数"""
        eobj = etree.HTML(html)
        li_list = eobj.xpath('//ul/li[@class="clear LOGVIEWDATA LOGCLICKDATA"]')
        for li in li_list:
            item = {}
            name_list = li.xpath('.//div[@class="positionInfo"]/a[1]/text()')
            item['name'] = name_list[0].strip() if name_list else None

            add_list = li.xpath('.//div[@class="positionInfo"]/a[2]/text()')
            item['add'] = add_list[0].strip() if add_list else None

            info_list = li.xpath('.//div[@class="houseInfo"]/text()')
            item['info'] = info_list[0].strip() if info_list else None

            total_list = li.xpath('.//div[@class="totalPrice"]/span/text()')
            item['total'] = total_list[0].strip() if total_list else None

            unit_list = li.xpath('.//div[@class="unitPrice"]/span/text()')
            item['unit'] = unit_list[0].strip() if unit_list else None

            print(item)
            # 数据存入MongoDB数据库
            self.myset.insert_one(item)

    def crawl(self):
        for pg in range(1, 101):
            page_url = self.url.format(pg)
            self.get_html(url=page_url)
            # 控制频率
            time.sleep(random.randint(1, 3))

if __name__ == '__main__':
    spider = LianjiaSpider()
    spider.crawl()
















































