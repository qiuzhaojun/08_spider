from selenium import webdriver
import time

class YdSpider:
    def __init__(self):
        # 无头
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(url='http://fanyi.youdao.com/')
        self.word = input('请输入要翻译的单词：')

    def translate(self):
        self.driver.find_element_by_xpath('//*[@id="inputOriginal"]').send_keys(self.word)
        # 给页面元素加载预留时间
        time.sleep(1)
        result = self.driver.find_element_by_xpath('//*[@id="transTarget"]/p/span').text
        self.driver.quit()

        return result

if __name__ == '__main__':
    spider = YdSpider()
    result = spider.translate()
    print(result)






























