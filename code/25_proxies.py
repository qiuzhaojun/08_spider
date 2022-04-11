"""

"""
import requests
from fake_useragent import UserAgent

url = 'http://httpbin.org/get'
headers = {'User-Agent':UserAgent().random}
proxies = {
    'http' : 'http://183.166.110.46:9999',
    'https': 'https://183.166.110.46:9999'
}

html = requests.get(url=url,
                    proxies=proxies,
                    headers=headers).text
# html:确认origin中对应IP到底是哪个?
print(html)



























