import pymysql
import requests

class Book:
    def __init__(self):
        self.url = "https://spa1.scrape.center/api/movie/?limit=10&offset=0"
        self.header = {
            "Accept":"application/json, text/plain, */*",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": "spa1.scrape.center",
            "Referer":"https://spa1.scrape.center/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows"
        }
        self.db = pymysql.Connect(
            host='localhost',
            port= 3306,
            user= 'root',
            password= '123456',
            database= 'scrapeBook',
        )

    # 获取html页面
    def get_html(self,url):
        result = requests.get(url=url,headers=self.header).json()
        return result

    # 爬虫逻辑函数
    def crawl(self):
        result = self.get_html(self.url)
        self.save_data(result)

    # 保存
    # def save(self,html):
    #     with open("book.html",'w') as f:
    #         f.write(html.text)
    def save_data(self,result):
        cur = self.db.cursor()
        for list in result['results']:
            book = [
                list['id'],
                list['name'],
                '|'.join(list['categories']),
                list['published_at'],
            ]
            cur.execute("insert into book values(%s,%s,%s,%s)",book)
            self.db.commit()


    def run(self):
        self.crawl()

if __name__ == "__main__":
    book = Book()
    book.run()