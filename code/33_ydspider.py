import requests
import json
import time
import random
from hashlib import md5

class YdSpider:
    def __init__(self):
        # F12抓包抓到的POST的地址
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.headers = {
            # 检查频率最高:Cookie Referer User-Agent
            "Cookie": "OUTFOX_SEARCH_USER_ID=-1868367574@103.102.194.226; OUTFOX_SEARCH_USER_ID_NCOO=1331175324.4029312; JSESSIONID=aaaj0sxGSruvg8elfwKzx; ___rl__test__cookies=1608004150725",
            "Referer": "http://fanyi.youdao.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        }

    def md5_str(self, s):
        """加密函数"""
        m = md5()
        m.update(s.encode())

        return m.hexdigest()

    def get_ts_salt_sign(self, word):
        # 获取ts salt sign
        ts = str(int(time.time() * 1000))
        salt = ts + str(random.randint(0, 9))
        s = "fanyideskweb" + word + salt + "]BjuETDhU)zqSxf-=B#7m"
        sign = self.md5_str(s)

        return ts, salt, sign

    def attack_yd(self, word):
        """爬虫逻辑函数"""
        ts, salt, sign = self.get_ts_salt_sign(word)
        data = {
            "i": word,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "lts": ts,
            "bv": "4f7ca50d9eda878f3f40fb696cce4d6d",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME",
        }
        # 请求解析提取数据
        html = requests.post(url=self.url,
                             data=data,
                             headers=self.headers).json()
        # json.loads():把json格式的字符串转为Python数据类型
        # html = json.loads(html)
        result = html['translateResult'][0][0]['tgt']
        print(result)

    def crawl(self):
        word = input('请输入要翻译的单词:')
        self.attack_yd(word)

if __name__ == '__main__':
    spider = YdSpider()
    spider.crawl()



