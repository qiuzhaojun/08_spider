"""
打开浏览器,输入百度的URL地址
"""
from selenium import webdriver

# 1.打开浏览器 - 创建浏览器对象
driver = webdriver.Chrome()
# 2.输入百度URL地址
driver.get(url='http://www.baidu.com/')
html = driver.page_source

driver.quit()




# 使用PhantomJS警告:
# Warning: selenium support for phantomjs
# has been desprecated, Please use headless
# versions of Chrome or Firefox instead























