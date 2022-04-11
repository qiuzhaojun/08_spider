"""
切换句柄
1. li = driver.window_handles
2. driver.switch_to.window(li[1])
"""
import sys
import time
from selenium import webdriver
import redis
from hashlib import md5

class MzbSpider:
    def __init__(self):
        self.url = 'http://www.mca.gov.cn/article/sj/xzqh/2020/'
        # 设置无界面
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(url=self.url)
        # 连接redis
        self.r = redis.Redis(host='localhost',
                             port=6380,
                             db=0)

    def md5_href(self, href):
        """功能函数"""
        m = md5()
        m.update(href.encode())

        return m.hexdigest()

    def parse_html(self):
        """爬虫逻辑函数"""
        # 1.找到最新月份节点并点击
        new_a = self.driver.find_element_by_xpath('//*[@id="list_content"]/div[2]/div/ul/table/tbody/tr[1]/td[2]/a')
        new_href = new_a.get_attribute('href')
        finger = self.md5_href(new_href)
        # redis增量判断
        if self.r.sadd('mzb:spiders', finger) == 1:
            new_a.click()
            time.sleep(1)
            # 2.切换句柄
            li = self.driver.window_handles
            self.driver.switch_to.window(li[1])
            # 3.提取具体数据
            tr_list = self.driver.find_elements_by_xpath('//tr[@height="19"]')
            for tr in tr_list:
                item = {}
                # selenium的xpath中坚决不能有 /text()  /@属性名
                # 获取文本: .text 属性
                # 获取属性值: .get_attribute('属性名')
                item['name'] = tr.find_element_by_xpath('./td[3]').text.strip()
                item['code'] = tr.find_element_by_xpath('./td[2]').text.strip()
                print(item)
        else:
            self.driver.quit()
            sys.exit('完成')

    def crawl(self):
        self.parse_html()

if __name__ == '__main__':
    spider = MzbSpider()
    spider.crawl()























