from selenium import webdriver
# 鼠标事件类
from selenium.webdriver import ActionChains

# 1.打开浏览器,输入百度地址
driver = webdriver.Chrome()
driver.get(url='http://www.baidu.com/')
# 2.先找到设置节点
node = driver.find_element_by_xpath('//*[@id="s-usersetting-top"]')
# 3.鼠标移动到设置节点
ActionChains(driver).move_to_element(node).perform()
# 4.找到高级搜索节点,并点击
driver.find_element_by_link_text('高级搜索').click()
















