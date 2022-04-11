"""
使用redis中的集合实现增量爬虫
思路:根据sadd的返回值来确定之前是否抓取过
    返回值1 : 说明之前没抓过,进行抓取!
    返回值0 : 说明之前已经抓过,结束程序!
"""
import requests
import re
import time
import random
import redis
from hashlib import md5
import sys

class GuaziSpider:
    def __init__(self):
        """定义常用变量"""
        self.url = 'https://www.guazi.com/bj/buy/o{}/#bread'
        self.headers = {
            'Cookie':'antipas=473ZM9X3528E27664Cc55; uuid=8df22213-560b-47cd-e60f-49bec9168257; clueSourceCode=%2A%2300; user_city_id=12; ganji_uuid=9654310392730175565240; sessionid=09250c0e-2fe5-40a9-8165-dcfc7b41af68; close_finance_popup=2020-10-14; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22self%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%228df22213-560b-47cd-e60f-49bec9168257%22%2C%22ca_city%22%3A%22bj%22%2C%22sessionid%22%3A%2209250c0e-2fe5-40a9-8165-dcfc7b41af68%22%7D; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A33434517385%7D; cityDomain=bj; preTime=%7B%22last%22%3A1602640004%2C%22this%22%3A1602638199%2C%22pre%22%3A1602638199%7D',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        }
        # 连接redis数据库
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def get_html(self, url):
        """功能函数1: 发请求获取响应内容"""
        html = requests.get(url=url, headers=self.headers).content.decode('utf-8')

        return html

    def re_func(self, regex, html):
        """功能函数2: 正则解析获取列表"""
        pattern = re.compile(regex, re.S)
        r_list = pattern.findall(html)

        return r_list

    def md5_url(self, url):
        """功能函数3: 对url地址进行md5加密"""
        s = md5()
        s.update(url.encode())

        return s.hexdigest()

    def parse_html(self, one_url):
        """爬虫逻辑函数 - 从一级页面开始抓取"""
        one_html = self.get_html(url=one_url)
        one_regex = '<li data-scroll-track=.*?href="(.*?)"'
        # href_list: ['/su/xxx', '/su/xxx', '', ..., '']
        href_list = self.re_func(one_regex, one_html)
        for href in href_list:
            two_url = 'https://www.guazi.com' + href
            finger = self.md5_url(url=two_url)
            # 返回值1:说明之前没抓过
            if self.r.sadd('guazi:spider', finger) == 1:
                # 获取一辆汽车详情页数据的函数
                self.get_one_car_info(two_url)
                # 控制频率
                time.sleep(random.randint(2, 3))
            else:
                # 彻底结束
                sys.exit('更新完成')

    def get_one_car_info(self, two_url):
        """获取一辆汽车的具体数据"""
        two_html = self.get_html(url=two_url)
        two_regex = '<div class="product-textbox">.*?<h2 class="titlebox">(.*?)</h2>.*?<li class="two"><span>(.*?)</span>.*?<li class="three"><span>(.*?)</span>.*?<li class="last"><span>(.*?)</span>.*?<span class="price-num">(.*?)</span>'
        # car_info_list: [('','','','','')]
        car_info_list = self.re_func(two_regex, two_html)
        item = {}
        item['name'] = car_info_list[0][0].strip().split('\r\n')[0]
        item['km'] = car_info_list[0][1].strip()
        item['displace'] = car_info_list[0][2].strip()
        item['type'] = car_info_list[0][3].strip()
        item['price'] = car_info_list[0][4].strip()
        print(item)

    def run(self):
        for o in range(1, 2):
            page_url = self.url.format(o)
            self.parse_html(one_url=page_url)

if __name__ == '__main__':
    spider = GuaziSpider()
    spider.run()











































