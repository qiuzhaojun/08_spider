from selenium import webdriver

# 1.打开浏览器
driver = webdriver.Chrome()
# 2.输入百度地址
driver.get(url='http://www.baidu.com/')
# 3.找到搜索框节点,并发送关键字:赵丽颖
node = driver.find_element_by_xpath('//*[@id="kw"]')
node.send_keys('赵丽颖')
# 4.找到百度一下按钮节点,并点击
driver.find_element_by_xpath('//*[@id="su"]').click()













