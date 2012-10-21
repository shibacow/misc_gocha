#!/usr/bin/python
# -*- coding:utf-8 -*-
#適当に、サンダーバードの、MLのファイルを探してそこを指定する。
mlsrc=u'C:/Documents and Settings/shibacow/Application Data/Thunderbird/Profiles/foubar/baz'
import os
import mailbox
from datetime import datetime,timedelta
from email.header import decode_header
import re
import csv

class Sender(object):
    def __init__(self,frm,sender,date):
        self.frm=self.split(unicode(frm))
        self.sender=sender
        self.date=self.parsedate(date)
    def __str__(self):
        return "from=%s sender=%s date=%s" % (self.frm.encode('cp932'),self.sender.encode('cp932'),self.date)
        #return self.frm
    def split(self,src):
        s=re.search('<(.*)>',src)
        if s:
            return s.group(1)
        else:
            return src

    def parsedate(self,date):
        date=re.sub(" [\+\-][\d]{4}.*",'',date)
        format=None
        if len(date.split(' '))==5:
            format="%a, %d %b %Y %H:%M:%S"
        elif len(date.split(' '))==4:
            format="%d %b %Y %H:%M:%S"
        return datetime.strptime(date,format)
        

def sender_pickup_in_annual(senders,frm,to):
    ys=[s for s in senders if frm< s.date <to]
    print "from=%s to=%s" % (frm,to)
    print "comment=%d" % len(ys)
    ysdict={}
    for s in ys:
        ysdict.setdefault(s.frm,s)
        ysdict[s.frm]=s
    sortlist=sorted(ysdict.items(),key=lambda x:x[1].date)
    fname='%s_%s.csv' % (frm.strftime('%Y-%m-%d'),to.strftime('%Y-%m-%d'))
    cw=csv.writer(open(fname,'wb'))
    cl=[]
    
    for s in sortlist:
        st=s[1]
        cl.append((st.frm.encode('utf-8'),st.sender.encode('utf-8'),st.date.strftime('%Y-%m-%d %H:%M:%S')))
    cw.writerows(cl)

def mailreader(path):
    senders=[]
    for message in mailbox.mbox(path):
        from_addr=message['from']
        frm=decode_header(from_addr)[0]
        sender=None
        if frm[1]:
            sender=unicode(frm[0],frm[1])
        else:
            sender=unicode(frm[0])
        date=message['date']
        senders.append(Sender(from_addr,sender,date))
    return senders

def main():
    if not os.path.exists(mlsrc):
        print u"%sは見つかりません" % mlsrc
        return 
    sender=mailreader(mlsrc)
    #for s in sender:
    #    print s
    print 'count=%d' % len(sender)
    now=datetime.now()
    tl=timedelta(days=365*3)
    org=now
    for _ in range(1):
        sender_pickup_in_annual(sender,org-tl,org)
        org=org-tl

    
if __name__=='__main__':main()
