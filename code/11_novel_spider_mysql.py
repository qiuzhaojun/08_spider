"""
笔趣阁小说数据抓取
1.小说链接
2.小说名称
3.小说作者
4.小说简介
"""
import requests
import re
import time
import random
import pymysql

class NovelSpider:
    def __init__(self):
        self.url = 'https://www.biqukan.cc/fenlei1/{}.html'
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        # 创建2个对象
        self.db = pymysql.connect(
            'localhost','root','123456',
            'noveldb',charset='utf8'
        )
        self.cur = self.db.cursor()

    def get_html(self, url):
        html = requests.get(url=url,
                            headers=self.headers).text
        # 直接调用解析函数
        self.parse_html(html)

    def parse_html(self, html):
        """正则解析函数"""
        regex = '<div class="caption">.*?href="(.*?)" title="(.*?)".*?<small class="text-muted fs-12">(.*?)</small>.*?>(.*?)</p>'
        novel_list = re.findall(regex,html,re.S)
        # 直接调用数据处理
        self.save_html(novel_list)

    def save_html(self, novel_list):
        """数据处理"""
        ins = 'insert into novel_tab values(%s,%s,%s,%s)'
        for one_novel_tuple in novel_list:
            li = [
                one_novel_tuple[1].strip(),
                one_novel_tuple[0].strip(),
                one_novel_tuple[2].strip(),
                one_novel_tuple[3].strip(),
            ]
            self.cur.execute(ins, li)
            # 提交到数据库执行
            self.db.commit()
            print(li)

    def crawl(self):
        for page in range(1, 3):
            page_url = self.url.format(page)
            self.get_html(url=page_url)
            # 控制数据抓取的频率
            time.sleep(random.randint(1, 3))

        # 所有页数据抓取完成后,断开数据库连接
        self.cur.close()
        self.db.close()

if __name__ == '__main__':
    spider = NovelSpider()
    spider.crawl()





























