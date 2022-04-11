"""
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

class NovelSpider:
    def __init__(self):
        self.url = 'https://www.biqukan.cc/fenlei1/{}.html'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

    def get_html(self, url):
        """功能函数1: 请求"""
        html = requests.get(url=url,
                            headers=self.headers).text

        return html

    def refunc(self, regex, html):
        """功能函数2:正则解析函数"""
        r_list = re.findall(regex, html, re.S)

        return r_list

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
            print(item)

    def run(self):
        for page in range(1, 3):
            page_url = self.url.format(page)
            self.crawl(page_url)
            # 控制频率
            time.sleep(random.randint(1, 3))

if __name__ == '__main__':
    spider = NovelSpider()
    spider.run()









































