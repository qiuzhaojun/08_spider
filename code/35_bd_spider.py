import re
import requests
import execjs

class BdTranslateSpider:
    def __init__(self):
        self.post_url = 'https://fanyi.baidu.com/v2transapi?from=en&to=zh'
        self.post_headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "content-length": "135",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": "BAIDUID=2562A9629D05E07784C35B687BF1C925:FG=1; BIDUPSID=2562A9629D05E07784C35B687BF1C925; PSTM=1591925907; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; MCITY=-131%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID_BFESS=C67151AAABF2EC202D3775C207F8D297:FG=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1607912557,1608000337,1608001755; delPer=0; PSINO=2; H_PS_PSSID=33213_1467_33222_33122_31254_32973_33286_33183_33181_32845_33198_33238_33217_33147_22158_33216_33215_33185; BA_HECTOR=8hak80aka4042k8kac1ftgou80q; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1608017864; ab_sr=1.0.0_MWVlZTlkMWVlY2NiN2E1NjEwY2VlYmIwYjJhNWYxNTU3YjNkYmIyZTU0MWNhOWUyNmRlYmYwNTQ3OGUxNmYxZDVlMzA0MDk0YjAxZGJkMDljOGJiZDgwZDkzMTJiYjc4; __yjsv5_shitong=1.0_7_270d02f07e4e2ba17cd3995b33b05adc22ef_300_1608017797596_106.38.76.26_946dfd73; yjs_js_security_passport=bda80b09b9e6be355a2c4a39b7e13fb96c551476_1608017798_js",
            "origin": "https://fanyi.baidu.com",
            "pragma": "no-cache",
            "referer": "https://fanyi.baidu.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }
        self.get_url = 'https://fanyi.baidu.com/'
        self.get_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "cookie": "BAIDUID=2562A9629D05E07784C35B687BF1C925:FG=1; BIDUPSID=2562A9629D05E07784C35B687BF1C925; PSTM=1591925907; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; MCITY=-131%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID_BFESS=C67151AAABF2EC202D3775C207F8D297:FG=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1607912557,1608000337,1608001755; delPer=0; PSINO=2; H_PS_PSSID=33213_1467_33222_33122_31254_32973_33286_33183_33181_32845_33198_33238_33217_33147_22158_33216_33215_33185; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1608022442; ab_sr=1.0.0_ODJmOTBkYWY0MWE0Y2Y4OTYwMjAyNWFmNGY1YmY3ZTRhYWUwNzE5N2I5Y2EwYWJhNjY5YWNjYjEzYjEyOWQzYTg3ZjhiNTViZDBkNzRhOTA0NmI2ZThhZDlmMGRkZDk5; __yjsv5_shitong=1.0_7_270d02f07e4e2ba17cd3995b33b05adc22ef_300_1608022382229_106.38.76.26_2dd0bb36; yjs_js_security_passport=9e30d406308dd2640b7bee80d29e44e803076831_1608022383_js",
            "pragma": "no-cache",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        }

    def get_gtk_token(self):
        html = requests.get(url=self.get_url,headers=self.get_headers).text
        gtk = re.findall("window.gtk = '(.*?)'", html, re.S)[0]
        token = re.findall("token: '(.*?)'", html, re.S)[0]

        return gtk, token

    def get_sign(self, word):
        # 获取sign: 利用execjs模块
        gtk, token = self.get_gtk_token()
        with open('translate.js', 'r') as f:
            jscode = f.read()

        jsobj = execjs.compile(jscode)
        sign = jsobj.eval(
            'e("{}","{}")'.format(word, gtk)
        )

        return sign

    def attack_yd(self, word):
        """爬虫逻辑函数"""
        sign = self.get_sign(word)
        print(sign)
        gtk, token = self.get_gtk_token()
        data = {
            "from": "en",
            "to": "zh",
            "query": word,
            "transtype": "realtime",
            "simple_means_flag": "3",
            "sign": sign,
            "token": token,
            "domain": "common",
        }
        html = requests.post(url=self.post_url,data=data,headers=self.post_headers).json()
        result = html['trans_result']['data'][0]['dst']
        print(result)

    def crawl(self):
        word = input('请输入翻译的单词:')
        self.attack_yd(word)

if __name__ == '__main__':
    spider = BdTranslateSpider()
    spider.crawl()




