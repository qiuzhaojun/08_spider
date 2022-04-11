from threading import Thread

# 线程事件函数
def spider():
    print('正在请求 解析 处理数据中...')

t_list = []
for i in range(5):
    t = Thread(target=spider)
    t_list.append(t)
    t.start()

for t in t_list:
    t.join()












