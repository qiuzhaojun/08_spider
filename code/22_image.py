import requests
from fake_useragent import UserAgent

url = "https://t7.baidu.com/it/u=1595072465,3644073269&fm=193&f=GIF"
headers = {'User-Agent':UserAgent().random}

html = requests.get(url=url, headers=headers).content
with open('girl.jpg', 'wb') as f:
    f.write(html)






