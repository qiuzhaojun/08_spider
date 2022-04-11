# 面试官: 为什么使用线程锁?
# 你: 因为多个线程在操作共享资源时会争夺资源,造成结果
    # 的不确定性
# 面试官: Python中不是有GIL吗,只能有一个线程执行,
    # 那是怎么争夺资源的?
# 你: 计算机执行代码时,会把一条语句拆成多条语句执行,
    # 同一个资源可能会被多个线程几乎同时操作,造成
    # 结果的不确定性

from threading import Thread,Lock

n = 5000
lock = Lock()

def f1():
    global n
    for i in range(1000000):
        lock.acquire()
        n += 1
        lock.release()

def f2():
    global n
    for i in range(1000000):
        lock.acquire()
        n -= 1
        lock.release()

t1 = Thread(target=f1)
t2 = Thread(target=f2)
t1.start()
t2.start()
t1.join()
t2.join()
print(n)

"""
# 正常： +1  -1
x = n + 1  # x=5001
n = x      # n=5001
x = n - 1  # x=5000
n = x      # n=5000

# 非正常: +1 -1
x = n + 1  # x=5001
x = n - 1  # x=4999
n = x      # n=4999
n = x      # n=4999
"""









