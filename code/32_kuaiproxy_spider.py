"""
库: proxydb
表: proxytab
表字段: id ip port
create database proxydb charset utf8;
use proxydb;
create table proxytab(
id int primary key auto_increment,
ip varchar(50),
port varchar(50)
)charset=utf8;
"""

import random
import time
import requests
from lxml import etree
from fake_useragent import UserAgent
import pymysql

class KuaiProxySpider:
    def __init__(self):
        self.get_url = 'https://www.kuaidaili.com/free/inha/{}/'
        self.test_url = 'http://httpbin.org/get'
        self.headers = {'User-Agent':UserAgent().random}
        # 连接数据库
        self.db = pymysql.connect('localhost', 'root', '123456', 'proxydb', charset='utf8')
        self.cur = self.db.cursor()

    def get_proxy(self, url):
        """获取代理IP"""
        html = requests.get(url=url, headers=self.headers).text
        eobj = etree.HTML(html)
        tr_list = eobj.xpath('//table/tbody/tr')
        for tr in tr_list:
            ip_list = tr.xpath('./td[1]/text()')
            port_list = tr.xpath('./td[2]/text()')
            if ip_list and port_list:
                # 测试此代理IP是否可用
                self.test_proxy(ip_list[0], port_list[0])
            else:
                print('此代理IP提取失败')

    def test_proxy(self, ip, port):
        """测试代理IP"""
        proxies = {
            'http':'http://{}:{}'.format(ip, port),
            'https':'https://{}:{}'.format(ip, port),
        }
        try:
            resp = requests.get(url=self.test_url,
                                proxies=proxies,
                                headers=self.headers,
                                timeout=3)
            if resp.status_code == 200:
                print(ip, port, '可用')
                ins = 'insert into proxytab(ip,port) values(%s,%s)'
                self.cur.execute(ins, [ip, port])
                self.db.commit()
            else:
                print(ip, port, '不可用')
        except Exception as e:
            print(ip, port, '不可用-')

    def crawl(self):
        for page in range(1, 1001):
            page_url = self.get_url.format(page)
            self.get_proxy(page_url)
            time.sleep(random.randint(1, 3))

        self.cur.close()
        self.db.close()

if __name__ == '__main__':
    spider = KuaiProxySpider()
    spider.crawl()


















