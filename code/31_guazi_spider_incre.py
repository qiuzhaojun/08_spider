"""
一级页面: 汽车链接
二级页面: 名称 行驶里程 排量 变速箱 价格
"""
import sys
import requests
from lxml import etree
import time
import random
import redis
from hashlib import md5

class GuaziSpider:
    def __init__(self):
        self.url = 'https://www.guazi.com/wx/buy/o{}/#bread'
        self.headers = {
            'Cookie': 'antipas=n58982r9c7529Oi3i07730612; uuid=12e2a817-882f-45b9-e8bb-608a957ed880; ganji_uuid=5409077541530572658244; clueSourceCode=%2A%2300; user_city_id=66; sessionid=2f183057-6d10-41ce-d7a8-595f85db2037; Hm_lvt_bf3ee5b290ce731c7a4ce7a617256354=1607572072,1607671115,1607677077,1607995433; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22self%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%2212e2a817-882f-45b9-e8bb-608a957ed880%22%2C%22ca_city%22%3A%22bj%22%2C%22sessionid%22%3A%222f183057-6d10-41ce-d7a8-595f85db2037%22%7D; close_finance_popup=2020-12-15; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A33892883372%7D; cityDomain=wx; preTime=%7B%22last%22%3A1607997183%2C%22this%22%3A1607572011%2C%22pre%22%3A1607572011%7D; Hm_lpvt_bf3ee5b290ce731c7a4ce7a617256354=1607997251',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        # 连接redis
        self.r = redis.Redis(host='127.0.0.1', port=6380, db=0)

    def get_html(self, url):
        """功能函数1"""
        html = requests.get(url=url,
                            headers=self.headers).content.decode('utf-8', 'ignore')

        return html

    def xfunc(self, html, x):
        """功能函数2"""
        eobj = etree.HTML(html)
        r_list = eobj.xpath(x)

        return r_list

    def md5_href(self, href):
        """功能函数3"""
        m = md5()
        m.update(href.encode())

        return m.hexdigest()

    def parse_html(self, first_url):
        """爬虫逻辑函数"""
        first_html = self.get_html(url=first_url)
        first_x = '//ul[@class="carlist clearfix js-top"]/li/a/@href'
        # href_list:['/sz/....','', ...]
        href_list = self.xfunc(first_html, first_x)
        for href in href_list:
            # 提取每辆汽车的信息
            finger = self.md5_href(href)
            if self.r.sadd('guazi:spiders', finger) == 1:
                # 开始抓
                self.get_car_info(href)
            else:
                sys.exit('更新完成')

    def get_car_info(self, href):
        """提取一辆汽车的具体数据"""
        second_url = 'https://www.guazi.com' + href
        second_html = self.get_html(url=second_url)
        second_x = '//div[@class="product-textbox"]'
        # one_div_list: [<element div at xxx>]
        one_div_list = self.xfunc(second_html, second_x)
        for one_div in one_div_list:
            item = {}
            name_list = one_div.xpath('./h1[@class="titlebox"]/text()')
            item['name'] = name_list[0].strip() if name_list else None

            km_list = one_div.xpath('.//li[@class="two"]/span/text()')
            item['km'] = km_list[0].strip() if km_list else None

            dis_list = one_div.xpath('.//li[@class="three"]/span/text()')
            item['dis'] = dis_list[0].strip() if dis_list else None

            type_list = one_div.xpath('.//li[@class="last"]/span/text()')
            item['type'] = type_list[0].strip() if type_list else None

            price_list = one_div.xpath('.//span[@class="price-num"]/text()')
            item['price'] = price_list[0].strip() if price_list else None

            print(item)

    def crawl(self):
        for o in range(1, 2):
            page_url = self.url.format(o)
            self.parse_html(page_url)
            time.sleep(random.randint(1, 3))

if __name__ == '__main__':
    spider = GuaziSpider()
    spider.crawl()




































