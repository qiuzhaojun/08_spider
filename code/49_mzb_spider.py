"""
切换句柄
1. li = driver.window_handles
2. driver.switch_to.window(li[1])
"""
import time

from selenium import webdriver

class MzbSpider:
    def __init__(self):
        self.url = 'http://www.mca.gov.cn/article/sj/xzqh/2020/'
        self.driver = webdriver.Chrome()
        self.driver.get(url=self.url)

    def parse_html(self):
        """爬虫逻辑函数"""
        # 1.找到最新月份节点并点击
        self.driver.find_element_by_xpath('//*[@id="list_content"]/div[2]/div/ul/table/tbody/tr[1]/td[2]/a').click()
        time.sleep(1)
        # 2.切换句柄
        li = self.driver.window_handles
        self.driver.switch_to.window(li[1])
        # 3.提取具体数据
        tr_list = self.driver.find_elements_by_xpath('//tr[@height="19"]')
        for tr in tr_list:
            print(tr.text)

    def crawl(self):
        self.parse_html()

if __name__ == '__main__':
    spider = MzbSpider()
    spider.crawl()























