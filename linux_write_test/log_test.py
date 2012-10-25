#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
logname='/ebs/log/myapp.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filename=logname,
    filemode='a')
import time
import os
import threading
mx=30000000
div=10000
def worker():
    count=0
    prevtime=time.time()
    prevcnt=count
    while count<mx:
        crr= threading.currentThread().getName()
        count+=1
        msg='crrthread=%s,cnt=%010d' % (crr,count)
        logging.info(msg)
        if count%div==0:
            tm=time.time()-prevtime
            diffcnt=count-prevcnt
            fsize=os.path.getsize(logname)
            fsize=fsize/(1024*1024)
            msg='crthreading=%s,count=%010d,diffcnt=%d,fsize=%d MB,time=%f' % \
                (crr,count,diffcnt,fsize,tm)
            print msg
            logging.info(msg)
            prevcnt=count
            prevtime=time.time()

threads=[]
for _ in range(10):
    t=threading.Thread(target=worker)
    threads.append(t)
    t.start()
