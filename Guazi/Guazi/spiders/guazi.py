# -*- coding: utf-8 -*-
import scrapy
from ..items import GuaziItem

class GuaziSpider(scrapy.Spider):
    name = 'guazi'
    allowed_domains = ['www.guazi.com']
    url = 'https://www.guazi.com/bj/buy/o{}/#bread'

    def get_cookies(self):
        """功能函数:处理cookie为字典"""
        cookstr = 'antipas=n58982r9c7529Oi3i07730612; uuid=12e2a817-882f-45b9-e8bb-608a957ed880; ganji_uuid=5409077541530572658244; clueSourceCode=%2A%2300; sessionid=2add5904-4928-4dc3-d86e-f76bba552701; close_finance_popup=2020-12-17; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22self%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%2212e2a817-882f-45b9-e8bb-608a957ed880%22%2C%22ca_city%22%3A%22bj%22%2C%22sessionid%22%3A%222add5904-4928-4dc3-d86e-f76bba552701%22%7D; cityDomain=bj; user_city_id=12; Hm_lvt_bf3ee5b290ce731c7a4ce7a617256354=1607671115,1607677077,1607995433,1608197832; preTime=%7B%22last%22%3A1608197766%2C%22this%22%3A1607572011%2C%22pre%22%3A1607572011%7D; Hm_lpvt_bf3ee5b290ce731c7a4ce7a617256354=1608197836'
        cookies = {}
        for kv in cookstr.split('; '):
            cookies[kv.split('=')[0]] = kv.split('=')[1]

        return cookies

    # 1.删掉start_urls变量
    # 2.重写start_urls()方法
    def start_requests(self):
        """生成所有要抓取的URL地址,交给调度器入队列"""
        for o in range(1, 6):
            page_url = self.url.format(o)
            # 交给调度器入队列
            yield scrapy.Request(
                url=page_url,
                callback=self.detail,
                cookies=self.get_cookies(),
            )

    def detail(self, response):
        """提取具体数据"""
        li_list = response.xpath('//ul[@class="carlist clearfix js-top"]/li')
        for li in li_list:
            # item:给items.py中GuaziItem类实例化
            item = GuaziItem()
            item['name'] = li.xpath('./a/@title').get()
            item['price'] = li.xpath('.//div[@class="t-price"]/p/text()').get()
            item['link'] = 'https://www.guazi.com' + li.xpath('./a/@href').get()

            # 把详情页链接继续交给调度器入队列
            # meta作用:不同解析函数间传递数据
            # meta随着请求先到调度器,然后到下载器,
            # 随着response一起交给callback解析函数
            yield scrapy.Request(
                url=item['link'],
                meta={'item':item},
                callback=self.get_car_info,
                cookies=self.get_cookies(),
            )

    def get_car_info(self, response):
        """二级页面解析函数:里程 排量 变速箱"""
        # 获取上个解析函数传递过来的item对象
        item = response.meta['item']

        item['km'] = response.xpath('//li[@class="two"]/span/text()').get()
        item['displace'] = response.xpath('//li[@class="three"]/span/text()').get()
        item['typ'] = response.xpath('//li[@class="last"]/span/text()').get()

        # 至此,一条完整的汽车数据提取完成,交给管道
        yield item













