"""
终端输入关键字,将百度的响应内容保存到本地文件
"""
import requests
from urllib import parse

# 1.拼接URL地址: http://www.baidu.com/s?wd=...
word = input('请输入关键字:')
params = parse.urlencode({'wd':word})
url = 'http://www.baidu.com/s?' + params
headers = {'User-Agent':'Mozilla/5.0'}

# 2.发请求获取响应
html = requests.get(url=url,
                    headers=headers).text

# 3.数据处理
filename = '{}.html'.format(word)
with open(filename, 'w',encoding='utf-8') as f:
    f.write(html)





























