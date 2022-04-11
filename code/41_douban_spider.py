"""
第一步实现: 抓取剧情类别下的所有电影,电影总数自动获取
第二步实现效果如下:
   剧情|喜剧|动作|爱情|...
   请输入电影类别: 喜剧
   # 效果:把所有喜剧的电影数据抓取完成
"""
import re

import requests
import json
import time
import random
from fake_useragent import UserAgent

class DouBanSpider:
    def __init__(self):
        self.url = 'https://movie.douban.com/j/chart/top_list?type={}&interval_id=100%3A90&action=&start={}&limit=20'

    def get_html(self, url):
        """功能函数"""
        headers = {'User-Agent':UserAgent().random}
        html = requests.get(url=url,
                            headers=headers).text

        return html

    def parse_html(self, url):
        """爬虫逻辑函数"""
        html = self.get_html(url)
        # html: [{},{}, ... , {}]
        html = json.loads(html)
        for one_film_dict in html:
            item = {}
            item['rank'] = one_film_dict['rank']
            item['title'] = one_film_dict['title']
            item['score'] = one_film_dict['score']
            item['time'] = one_film_dict['release_date']
            item['type'] = one_film_dict['types']
            print(item)

    def get_total(self, user_type):
        """获取某个类别下的电影总数"""
        total_url = 'https://movie.douban.com/j/chart/top_list_count?type={}&interval_id=100%3A90'.format(user_type)
        total_html = self.get_html(total_url)
        total_html = json.loads(total_html)
        total = total_html['total']

        return total

    def get_all_type_dict(self):
        """返回所有类别的大字典"""
        index_url = 'https://movie.douban.com/chart'
        index_html = self.get_html(index_url)
        regex = '<span><a href=".*?type_name=(.*?)&type=(.*?)&interval_id=100:90&action=">'
        # r_list: [('剧情','11'),('喜剧','23'), ...]
        r_list = re.findall(regex, index_html, re.S)
        all_type_dict = {}
        for r in r_list:
            all_type_dict[r[0]] = r[1]

        return all_type_dict

    def crawl(self):
        # 用户输入: 喜剧
        # 想办法拿到: 喜剧对应的type的值
        # {'剧情':'11', '喜剧':'24',...}
        all_type_dict = self.get_all_type_dict()
        # 终端提示
        menu = ''
        for k in all_type_dict:
            menu += k + '|'
        print(menu)
        # 接收用户输入
        user_c = input('请输入类别:')
        user_type = all_type_dict[user_c]
        # 获取user_type电影总数量
        total = self.get_total(user_type)
        for start in range(0, total, 20):
            page_url = self.url.format(user_type, start)
            self.parse_html(url=page_url)
            # 控制频率
            time.sleep(random.randint(0,1))

if __name__ == '__main__':
    spider = DouBanSpider()
    spider.crawl()