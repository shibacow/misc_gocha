#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
import time
import os
logname='/ebs/log/myapp.log'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=logname,
                    filemode='a')

mx=300000000
count=0
div=100000
prevtime=time.time()
prevcnt=count
while count<mx:
    count+=1
    msg='cnt=%010d' % count
    logging.info(msg)
    if count%div==0:
        tm=time.time()-prevtime
        diffcnt=count-prevcnt
        fsize=os.path.getsize(logname)
        fsize=fsize/(1024*1024)
        msg='count=%010d,diffcnt=%d,fsize=%d MB,time=%f' % (count,diffcnt,fsize,tm)
        print msg
        logging.info(msg)
        prevcnt=count
        prevtime=time.time()



