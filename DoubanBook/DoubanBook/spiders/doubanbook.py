import scrapy
from ..items import DoubanbookItem

class DoubanbookSpider(scrapy.Spider):
    name = 'doubanbook'
    allowed_domains = ['https://www.18600.org/top/hot4.html']
    # start_urls = ['http://https://book.douban.com/top250/']

    def start_requests(self):
        """生成所有要抓取的URL地址,一次性交给调度器入队列"""
        for i in range(1,3):
            # url = 'http://xiangmuhezuo.huangye88.com/xingyehezuo/diannaoxiangmuhezuo/pn{}'.format(i)
            url = "https://www.18600.org/top/hot4.html"
            # scrapy.Request(): 把请求交给调度器入队列
            yield scrapy.Request(url=url,
                                 callback=self.parse)

    def parse(self, response):
        li_list = response.xpath("//tbody//td[@class='w345']/a/@title")
        item = DoubanbookItem()
        for li in li_list:
            item['name'] = li.get()
            yield item