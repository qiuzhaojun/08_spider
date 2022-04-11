import requests
import pymysql
from lxml import etree
from hashlib import md5

class DoubanbookSpider:
    def __init__(self):
        # 初始化url，数据库参数等
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='123456',
                                  database='douban_book',
                                  charset='utf8')
        self.cur = self.db.cursor()

    def get_html(self,url):
        # 请求
        html = requests.get(url=url,
                            headers = self.header).content.decode('utf-8','ignore')
        return html

    def path(self,html,xpath):
        # 创建解析对象
        p = etree.HTML(html)
        # 调用解析对象
        list = p.xpath(xpath)
        return list

    def run(self):
        # 运行爬虫程序
        first_html = self.get_html("https://book.douban.com/top250")
        second_url_list = self.path(first_html,"//div[@class='indent']//a[@class='nbg']/@href")
        for second_url in second_url_list:
            book = {}
            second_html = self.get_html(second_url)
            # 获取书名
            book_name = self.path(second_html,"//*[@id='wrapper']/h1/span/text()")
            book['name'] = book_name[0] if book_name else None
            # 获取评分
            book_score = self.path(second_html,"//*[@id='interest_sectl']/div/div[2]/strong/text()")
            book['score'] = book_score[0] if book_score else None
            # 存入数据库
            self.save_data(book)
            pass

    def md5_href(self,href):
        m = md5()
        m.update(href.encode())
        return m.hexdigest()

    def save_data(self,dict):
        md5_book = self.md5_href(dict['name'])
        ins = "select * from book where request_finger=%s"
        self.cur.execute(ins,md5_book)
        result = self.cur.fetchall()
        if not result:
            # 存入数据库
            ins = "insert into book(name,score,request_finger) values(%s,%s,%s)"
            self.cur.execute(ins,[dict['name'],dict['score'],md5_book])
            self.db.commit()
            print("%已抓取并存入数据库"%dict['name'])
        else:
            print("%s已经抓取过"%dict['name'])

if __name__ == "__main__":
    doubanbook = DoubanbookSpider()
    doubanbook.run()
