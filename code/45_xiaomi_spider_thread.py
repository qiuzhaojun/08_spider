"""
多线程抓取小米应用商店-聊天社交下应用信息
何处加锁?
    当多个线程操作全局变量时,需要加锁
"""
import requests
import time
from threading import Thread, Lock
from queue import Queue
from fake_useragent import UserAgent

class XiaoMiSpider:
    def __init__(self):
        self.url = 'https://app.mi.com/categotyAllListApi?page={}&categoryId=2&pageSize=30'
        # 队列 锁
        self.q = Queue()
        self.lock = Lock()

    def url_to_q(self):
        """生成所有待爬取的URL地址,先入队列"""
        for page in range(67):
            page_url = self.url.format(page)
            # 入队列!
            self.q.put(page_url)

    def get_html(self, url):
        """功能函数"""
        headers = {'User-Agent':UserAgent().random}
        html = requests.get(url=url,
                            headers=headers).json()

        return html

    def parse_html(self):
        """线程事件函数:获取地址 请求 解析 数据处理"""
        # q: ['http://last.html']
        # Thread-1: 判断不为空,但是还没get()
        # Thread-2: 判断不为空,进入if分支里面
        while True:
            # 加锁
            self.lock.acquire()
            if not self.q.empty():
                url = self.q.get()
                # 释放锁
                self.lock.release()
                html = self.get_html(url)
                for one_app_dict in html['data']:
                    item = {}
                    item['name'] = one_app_dict['displayName']
                    item['type'] = one_app_dict['level1CategoryName']
                    item['link'] = one_app_dict['packageName']
                    print(item)
            else:
                # 释放锁
                self.lock.release()
                break

    def crawl(self):
        # 先让URL地址入队列
        self.url_to_q()
        # 创建多线程
        t_list = []
        for i in range(1):
            t = Thread(target=self.parse_html)
            t_list.append(t)
            t.start()

        for t in t_list:
            t.join()

if __name__ == '__main__':
    start = time.time()
    spider = XiaoMiSpider()
    spider.crawl()
    end = time.time()
    print('time:%.2f' % (end - start))




























