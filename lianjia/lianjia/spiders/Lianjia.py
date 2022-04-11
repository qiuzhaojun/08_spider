import scrapy


class LianjiaSpider(scrapy.Spider):
    name = 'Lianjia'
    allowed_domains = ['wwww.lianjia.com']
    start_urls = ['http://wwww.lianjia.com/']

    def parse(self, response):
        pass
