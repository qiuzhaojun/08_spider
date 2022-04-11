"""
mysql实现增量爬虫
多级页面数据抓取
    *********一级页面需抓取***********
        1、小说名称
        2、小说详情页链接
        3、小说作者
        4、小说描述

    *********二级页面需抓取***********
        1、全部的章节名称
        2、全部的章节链接
"""
import requests
import re
import time
import random
import pymysql
from hashlib import md5

class NovelSpider:
    def __init__(self):
        self.url = 'https://www.biqukan.cc/fenlei1/{}.html'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        # 连接MySQL
        self.db = pymysql.connect('localhost', 'root', '123456', 'noveldb', charset='utf8')
        self.cur = self.db.cursor()

    def get_html(self, url):
        """功能函数1: 请求"""
        html = requests.get(url=url,
                            headers=self.headers).text

        return html

    def refunc(self, regex, html):
        """功能函数2:正则解析函数"""
        r_list = re.findall(regex, html, re.S)

        return r_list

    def md5_href(self, href):
        m = md5()
        m.update(href.encode())

        return m.hexdigest()

    def crawl(self, first_url):
        """爬虫逻辑函数"""
        first_html = self.get_html(url=first_url)
        first_regex = '<div class="caption">.*?<a href="(.*?)" title="(.*?)">.*?<small.*?>(.*?)</small>.*?>(.*?)</p>'
        first_list = self.refunc(first_regex,
                                 first_html)
        for one_novel_tuple in first_list:
            item = {}
            item['title'] = one_novel_tuple[1].strip()
            item['href'] = one_novel_tuple[0].strip()
            item['author'] = one_novel_tuple[2].strip()
            item['comment'] = one_novel_tuple[3].strip()
            # 获取此本小说中剩余的数据
            self.parse_second_page(item)

    def parse_second_page(self, item):
        """二级页面解析函数"""
        # 全部章节名称 和 链接
        second_html = self.get_html(url=item['href'])
        second_regex = '<dd class="col-md-4"><a href="(.*?)">(.*?)</a></dd>'
        # second_list: [('女人','href'),(),...]
        second_list = self.refunc(second_regex,second_html)
        for second_tuple in second_list:
            item['son_title'] = second_tuple[1]
            item['son_href'] = second_tuple[0]
            # 生成指纹
            finger = self.md5_href(item['son_href'])
            sel = 'select * from request_finger where finger=%s'
            self.cur.execute(sel, [finger])
            # result情况1: (('def23232'),)
            # result情况2: 空元组
            result = self.cur.fetchall()
            if not result:
                print('进行抓取:', item['son_title'])
                # 把finger放到指纹表中
                ins = 'insert into request_finger values(%s)'
                self.cur.execute(ins, [finger])
                self.db.commit()
            else:
                print('已经抓取过')

    def run(self):
        for page in range(1, 3):
            page_url = self.url.format(page)
            self.crawl(page_url)
            # 控制频率
            time.sleep(random.randint(1, 3))

        self.cur.close()
        self.db.close()

if __name__ == '__main__':
    spider = NovelSpider()
    spider.run()









































