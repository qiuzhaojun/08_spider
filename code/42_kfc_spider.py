"""
create database kfcdb charset utf8;
use kfcdb;
create table kfctab(
rownum varchar(200),
storeName varchar(200),
cityName varchar(200),
provinceName varchar(200),
addressDetail varchar(200),
pro varchar(200)
)charset=utf8;
"""

import requests
import time
import random
from fake_useragent import UserAgent
import pymysql

class KfcSpider:
    def __init__(self):
        self.url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname'
        self.city = input('请输入城市:')
        # 创建2个对象
        self.db = pymysql.connect('localhost', 'root', '123456', 'kfcdb', charset='utf8')
        self.cur = self.db.cursor()

    def get_html(self, data):
        headers = {'User-Agent':UserAgent().random}
        html = requests.post(url=self.url,
                             data=data,
                             headers=headers).json()

        return html

    def get_total_page(self):
        data = {
            'cname': self.city,
            'pid': '',
            'pageIndex': '1',
            'pageSize': '10',
        }
        total_html = self.get_html(data)
        count = total_html['Table'][0]['rowcount']
        total_page = count//10 if count%10==0 else count//10 + 1

        return total_page

    def parse_html(self):
        """爬虫逻辑函数"""
        # all_city_list: ['', '', '', ...]
        # for one_city in all_city_list:
        total_page = self.get_total_page()
        for page in range(1, total_page + 1):
            data = {
                'cname': self.city,
                'pid': '',
                'pageIndex': str(page),
                'pageSize': '10',
            }
            html = self.get_html(data)
            for one_shop_dict in html['Table1']:
                item = {}
                item['rownum'] = one_shop_dict['rownum']
                item['storeName'] = one_shop_dict['storeName']
                item['cityName'] = one_shop_dict['cityName']
                item['provinceName'] = one_shop_dict['provinceName']
                item['addressDetail'] = one_shop_dict['addressDetail']
                item['pro'] = one_shop_dict['pro']
                print(item)
                # 存入数据
                ins = 'insert into kfctab values(%s,%s,%s,%s,%s,%s)'
                li = [item['rownum'], item['storeName'], item['cityName'], item['provinceName'], item['addressDetail'], item['pro']]
                self.cur.execute(ins, li)
                self.db.commit()
            # 控制频率
            time.sleep(random.randint(1, 2))

    def crawl(self):
        self.parse_html()
        self.cur.close()
        self.db.close()

if __name__ == '__main__':
    spider = KfcSpider()
    spider.crawl()













