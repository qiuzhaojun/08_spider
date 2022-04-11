"""
向京东官网发请求,拿到响应内容
"""
import requests

resp = requests.get(url='https://www.jd.com/')
# text属性: 获取响应内容 - 字符串
html = resp.text
# content属性: 获取响应内容 - 字节串,图片、文件...
html = resp.content
# status_code属性: HTTP响应码
code = resp.status_code
# url属性: 返回实际数据的url地址
url = resp.url
print(code, url)
































