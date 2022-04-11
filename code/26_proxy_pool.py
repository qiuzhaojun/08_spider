"""
建立代理IP池 - 开放代理
1.获取到代理IP
2.依次测试,能用的保存,不能用的舍弃
"""
import requests
from fake_useragent import UserAgent


class ProxyPool:
    def __init__(self):
        self.api_url = 'http://dev.kdlapi.com/api/getproxy/?orderid=970793674390459&num=20&protocol=2&method=1&an_ha=1&sep=1'
        self.test_url = 'http://httpbin.org/get'
        self.headers = {'User-Agent':UserAgent().random}

    def get_proxy(self):
        html = requests.get(url=self.api_url,headers=self.headers).text
        # 目标:['1.1.1.1:8888', '', '', ...]
        proxy_list = html.split('\r\n')
        for proxy in proxy_list:
            # 测试每个代理IP是否可用
            self.test_proxy(proxy)

    def test_proxy(self, proxy):
        """测试1个代理IP是否可用"""
        proxies = {
            'http':'http://{}'.format(proxy),
            'https':'https://{}'.format(proxy)
        }
        try:
            resp = requests.get(url=self.test_url,
                                headers=self.headers,
                                proxies=proxies,
                                timeout=3)
            if resp.status_code == 200:
                print(proxy,'\033[31m可用\033[0m')
            else:
                print(proxy,'不可用-')
        except Exception as e:
            print(proxy, '不可用')

    def crawl(self):
        self.get_proxy()

if __name__ == '__main__':
    spider = ProxyPool()
    spider.crawl()




















