# coding=utf-8

import threading
from time import sleep


def music(func):
    for i in range(10):
        print("a", end='-')
        sleep(0.5)


def move(func):
    for i in range(5):
        print("b", end='-')
        sleep(0.5)

threads = []
print("music start")
import DataFlow
data_flow = DataFlow.DataFlow('37', '7')
t1 = threading.Thread(target=data_flow.read_dht11(), args=(u'爱情买卖',))
print("music end")
threads.append(t1)
print("move start")
t2 = threading.Thread(target=move, args=(u'阿凡达',))
print("move end")
threads.append(t2)

# 子进程结束完,父进程才结束
if __name__ == '__main__':
    # for t in threads:
        # t.setDaemon(True)
        # t.start()
    for t in threads:
        t.join()
print("all over")
