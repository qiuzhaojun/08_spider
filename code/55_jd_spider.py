"""
driver.execute_script('JS脚本')
"""
from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get(url='https://search.jd.com/Search?keyword=%E8%B5%B5%E4%B8%BD%E9%A2%96&enc=utf-8&suggest=1.his.0.0&wq=&pvid=a9f19134b4684a5582408f842c402b5d')

# 执行JS脚本
driver.execute_script(
    'window.scrollTo(0,document.body.scrollHeight)'
)
# 给页面元素的加载预留时间
time.sleep(3)
# 提取数据
li_list = driver.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li')
for li in li_list:
    item = {}
    info_list = li.text.split('\n')
    # 情况1: 价格 名称 评价 商家
    if info_list[0].startswith('￥'):
        item['price'] = info_list[0]
        item['name'] = info_list[1]
        item['commit'] = info_list[2]
        item['shop'] = info_list[3]
    # 情况2: <  >  价格 名称 评价 商家
    elif info_list[0].startswith('<'):
        item['price'] = info_list[2]
        item['name'] = info_list[3]
        item['commit'] = info_list[4]
        item['shop'] = info_list[5]
    # 情况3: 每满..  <  >  价格 名称 评价 商家
    elif info_list[0].startswith('每满') and info_list[1].startswith('<'):
        item['price'] = info_list[3]
        item['name'] = info_list[4]
        item['commit'] = info_list[5]
        item['shop'] = info_list[6]
    # 情况4: 每满..  价格 名称 评价 商家
    else:
        item['price'] = info_list[1]
        item['name'] = info_list[2]
        item['commit'] = info_list[3]
        item['shop'] = info_list[4]

    print(item)



driver.quit()














