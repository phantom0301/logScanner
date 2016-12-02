#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Phantom0301
__author__ = 'Phantom0301'
"""
大文件读取
"""

from performMonitor import per_mon
import os
import glob
import fileinput
import linecache
import Queue
import threading

from logs_parsers import apache_log_parser

exitFlag = 0
threads=[]


def path_traversal(file_path):
    file_list = []
    for f in os.walk(file_path):
        for line in f[2]:
             file_list.append(f[0]+"\\"+line)
    return file_list

'''
def path_traversal_by_glob(file_path):  # glob测试中性能不如walk
    file_list = []
    path = os.path.expanduser(file_path)
    for f in glob.glob(path + '/*'):
        file_list.append(f)
    return file_list
'''

def read_in_block(file_path):
    BLOCK_SIZE = 4096
    with open(file_path, 'r') as f:
        while True:
            block = f.read(BLOCK_SIZE)  # 每次读取固定长度到缓冲区
            if block:
                yield block
            else:
                return  # 读取到文件末尾则退出

#@per_mon
def read(file_path):
    for block in read_in_block(file_path):
        pass
'''
@per_mon
def read_in_line(file_path):
    with open(file_path) as f:
        for line in f:
            print line

@per_mon
def read_in_fileinput(file_path):  # 性能和in_line相似
    for eachline in fileinput.input(file_path):
        print eachline

@per_mon
def read_in_linecache(file_path):
    cache_data = linecache.getlines(file_path)
    for line in range(len(cache_data)):
        print cache_data[line]

@per_mon
def test():
    file_lists = path_traversal('D:\W3SVC1\TEST')
    for name in file_lists:
        read(name)
'''
class readThread(threading.Thread):
    def __init__(self, threadID,q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.q = q
    def run(self):
        while not self.q.empty():
            path = self.q.get()
            read(path)

@per_mon
def test1():
    workQueue = Queue.Queue()
    threadLock = threading.Lock()
    file_lists = path_traversal('D:\W3SVC1\TEST')
    threadLock.acquire()
    for path in file_lists:
        workQueue.put(path)
    for i in range(10):
        thread = readThread(i, workQueue)
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join(10)
        t.stop()


if __name__ == "__main__":
    line_parser = apache_log_parser. make_parser('''%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"''')
    file_lists = path_traversal('C:\Users\phantom\Desktop\\apache_log_myself')
    import pymongo
    from pymongo import MongoClient

    client = MongoClient()
    db = client['mylog']
    collection = db.apache_access
    for path in file_lists:
        f = open(path, 'r')
        for line in f:
            log_line_data = line_parser(line)
            collection.insert(log_line_data)
        f.close()







