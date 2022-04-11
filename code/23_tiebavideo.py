"""
1.先从帖子中提取视频链接
2.向视频链接发请求,将视频保存到本地
"""
import requests
from lxml import etree
from fake_useragent import UserAgent
import os

# 1.提取视频链接
url = 'https://tieba.baidu.com/p/7146936032'
headers = {'User-Agent':UserAgent().random}
html = requests.get(url=url,
                    headers=headers).content.decode('utf-8', 'ignore')

filename = 'video.html'
with open(filename, 'w') as f:
    f.write(html)

# xpath提取链接
eobj = etree.HTML(html)
src = eobj.xpath('//div[@class="video_src_wrapper"]/embed/@data-video')[0]

# 创建保存目录结构
directory = '/home/tarena/video/'
if not os.path.exists(directory):
    os.makedirs(directory)

# 将视频保存到本地文件
video_html = requests.get(url=src,
                          headers=headers).content
filename = '{}{}.mp4'.format(directory,src[-20:])
with open(filename, 'wb') as f:
    f.write(video_html)







































