"""
第一步实现: 抓取剧情类别下的所有电影,电影总数自动获取
第二步实现效果如下:
   剧情|喜剧|动作|爱情|...
   请输入电影类别: 喜剧
   # 效果:把所有喜剧的电影数据抓取完成
"""

import requests
import json
import time
import random
from fake_useragent import UserAgent

class DouBanSpider:
    def __init__(self):
        self.url = 'https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start={}&limit=20'

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

    def get_total(self):
        """获取某个类别下的电影总数"""
        pass

    def crawl(self):
        total = self.get_total()
        for start in range(0, total, 20):
            page_url = self.url.format(start)
            self.parse_html(url=page_url)
            # 控制频率
            time.sleep(random.randint(0,1))

if __name__ == '__main__':
    spider = DouBanSpider()
    spider.crawl()
























