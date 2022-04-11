from selenium import webdriver

# 1.打开浏览器,输入主页地址
driver = webdriver.Chrome()
driver.get(url='https://music.163.com/#/discover/toplist')
# 2.切换iframe
driver.switch_to.frame("contentFrame")
# 3.提取数据 : item={}
tr_list = driver.find_elements_by_xpath('//table/tbody/tr')
for tr in tr_list:
    item = {}
    item['rank'] = tr.find_element_by_xpath('.//span[@class="num"]').text
    item['name'] = tr.find_element_by_xpath('.//span[@class="txt"]/a/b').get_attribute('title').replace('\xa0', ' ')
    item['time'] = tr.find_element_by_xpath('.//span[@class="u-dur "]').text
    item['singer'] = tr.find_element_by_xpath('.//div[@class="text"]/span').get_attribute('title')
    print(item)

driver.quit()


