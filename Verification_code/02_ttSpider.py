from ttapi import base64_api
from selenium import webdriver
# python图片处理库
from PIL import Image

class TTLogin:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get(url='http://www.ttshitu.com/login.html?spm=null')

    def get_image(self):
        # 1.先获取背景图 - 登录页的图
        self.driver.save_screenshot('index.png')
        # 2.再截取验证码图
        # location: 获取节点左上角的 x y 坐标
        locate = self.driver.find_element_by_xpath('//*[@id="captchaImg"]').location
        left_x = locate['x']
        left_y = locate['y']
        # size属性: 获取节点的宽度width和高度height
        siz = self.driver.find_element_by_xpath('//*[@id="captchaImg"]').size
        right_x = left_x + siz['width']
        right_y = left_y + siz['height']
        # 截取图片
        img = Image.open('index.png').crop((left_x,left_y,right_x,right_y))
        img.save('image.png')
        # 调用在线打码
        result = base64_api('hacker001', 'zhanshen001', 'image.png')

        return result

    def crawl(self):
        result = self.get_image()
        self.driver.find_element_by_xpath('/html/body/div/div/div[2]/form/div[1]/input').send_keys('hacker001')
        self.driver.find_element_by_xpath('/html/body/div/div/div[2]/form/div[2]/input').send_keys('zhanshen001')
        self.driver.find_element_by_xpath('/html/body/div/div/div[2]/form/div[3]/div[1]/input').send_keys(result)
        self.driver.find_element_by_xpath('/html/body/div/div/div[2]/form/button').click()


if __name__ == '__main__':
    spider = TTLogin()
    spider.crawl()































