import re
import sys
import requests
from lxml import etree
from hashlib import md5
import redis

class MzbSpider:
    def __init__(self):
        self.url = 'http://www.mca.gov.cn/article/sj/xzqh/2020/'
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        self.r = redis.Redis(host='localhost', port=6380, db=0)

    def get_html(self, url):
        """功能函数1"""
        html = requests.get(url=url,
                            headers=self.headers).content.decode('utf-8', 'ignore')

        return html

    def md5_href(self, href):
        """功能函数2"""
        m = md5()
        m.update(href.encode())

        return m.hexdigest()

    def xfunc(self, html, x):
        """功能函数3"""
        eobj = etree.HTML(html)
        r_list = eobj.xpath(x)

        return r_list

    def parse_html(self):
        """爬虫逻辑函数,先提取最新月份href"""
        html = self.get_html(url=self.url)
        x = '//table/tr[1]/td[@class="arlisttd"]/a/@href'
        href_list = self.xfunc(html, x)
        if href_list:
            new_url = 'http://www.mca.gov.cn' + href_list[0]
            finger = self.md5_href(new_url)
            if self.r.sadd('mzb:spiders', finger) == 1:
                # 开始获取真实返回数据的链接
                self.get_real_url(new_url)
            else:
                # 结束
                sys.exit('完成!!')
        else:
            print('提取最新月份链接失败')

    def get_real_url(self, new_url):
        """提取真实返回数据的链接"""
        html = self.get_html(url=new_url)
        regex = 'window.location.href="(.*?)"'
        real_url_list = re.findall(regex, html, re.S)
        if real_url_list:
            # 开抓
            real_url = real_url_list[0]
            self.get_data(real_url)
        else:
            print('提取真实链接失败')

    def get_data(self, real_url):
        """提取具体数据的函数"""
        html = self.get_html(url=real_url)
        x = '//tr[@height="19"]'
        tr_list = self.xfunc(html, x)
        for tr in tr_list:
            item = {}
            item['name'] = tr.xpath('./td[3]/text()')[0].strip()
            item['code'] = tr.xpath('./td[2]/text() | ./td[2]/span/text()')[0].strip()
            print(item)

    def crawl(self):
        self.parse_html()

if __name__ == '__main__':
    spider = MzbSpider()
    spider.crawl()















