#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
import time
import os
logname='/ebs/log/myapp.log'
log_file=open(logname,'ab')
mx=300000000
count=0
div=100000
prevtime=time.time()
prevcnt=count
while count<mx:
    count+=1
    msg='cnt=%010d\n' % count
    log_file.write(msg)
    log_file.flush()
    if count%div==0:
        tm=time.time()-prevtime
        diffcnt=count-prevcnt
        fsize=os.path.getsize(logname)
        fsize=fsize/(1024*1024)
        msg='count=%010d,diffcnt=%d,fsize=%d MB,time=%f\n' % (count,diffcnt,fsize,tm)
        log_file.write(msg)
        log_file.flush()
        print msg
        prevcnt=count
        prevtime=time.time()



