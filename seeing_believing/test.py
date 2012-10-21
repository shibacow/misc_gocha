#!/usr/bin/python
import random,time,sys
from sort_test import list_sort
## a=(11,2,12)
## b=(14,33,21)
## c=(12,14,66)
## d=(22,11,2)
## e=(4,9,11)
## f=(9,8,12)
## g=(3,8,7)
## l=[c,b,a,d,e,f,g]
## print l
## l2=list_sort(l,len(l))
## for k in l2:
##     j=k[0]+k[1]+k[2]
##    print '%s%d' % (str(k),j),
##print 
## for i in l2:
##    print i,
## l=range(1000)
## random.shuffle(l)
## t1=time.time()
## l2=list_sort(l,len(l))
## t1=(time.time()-t1)*1000
## print 'native %d' % t1
## l=range(1000)
## random.shuffle(l)
## t1=time.time()
## l.sort()
## t1=(time.time()-t1)*1000
## print 'python %d' % t1
if sys.argv[1:]==[]:
    print 'usage:',sys.argv[0],'number'
    sys.exit(1)
if int(sys.argv[1])==0:
    print 'sys.argv',sys.argv[1],'invalid'

MAX=int(sys.argv[1])
rgblist=[]
for i in range(MAX):
    r=g=b=0
    r=random.randint(0,255)
    g=random.randint(0,255)
    b=random.randint(0,255)
    rgb=(r,g,b)
    rgblist.append(rgb)
t1=time.time()
l2=list_sort(rgblist,len(rgblist))
t1=(time.time()-t1)*1000
##print l2
## for k in l2:
##    j=k[0]+k[1]+k[2]
##   print j,
print 'ntime=%d' % t1
rgblist=[]
for i in range(MAX):
    r=g=b=0
    r=random.randint(0,255)
    g=random.randint(0,255)
    b=random.randint(0,255)
    rgb=(r,g,b)
    rgblist.append(rgb)
t1=time.time()
rgblist.sort(lambda x,y:cmp(x[0]+x[1]+x[2],y[0]+y[1]+y[2]))
t1=(time.time()-t1)*1000
print 'ptime=%d' % t1
