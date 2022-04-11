# -*- coding: utf-8 -*-
import scrapy
from ..items import MaoyanItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/board/4']

    def parse(self, response):
        dd_list = response.xpath('//dl/dd')
        for dd in dd_list:
            item = MaoyanItem()
            item['name'] = dd.xpath('.//p[@class="name"]/a/text()').get()
            item['star'] = dd.xpath('.//p[@class="star"]/text()').get()
            item['time'] = dd.xpath('.//p[@class="releasetime"]/text()').get()

            # 交给管道文件
            yield item

# 进程 线程 协程
# 协程: 微线程 纤程
# yield语句实现协程的关键字
# 实现协程的模块: gevent greenlet






