import requests
import re

url = 'https://maoyan.com/board/4'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

html = requests.get(url=url, headers=headers).text

regex = '<div class="movie-item-info">.*?title="(.*?)".*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>'
r_list = re.findall(regex, html, re.S)
for r in r_list:
    print(r)








