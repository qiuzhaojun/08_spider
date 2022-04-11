# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GuaziItem(scrapy.Item):
    # define the fields for your item here like:
    # 一级页面
    name = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    # 二级页面
    km = scrapy.Field()
    displace = scrapy.Field()
    typ = scrapy.Field()




# 相当于 {'name':'', 'price':'', 'link':''}
