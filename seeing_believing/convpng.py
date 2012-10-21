#!/usr/bin/python
from sort_test import list_sort
import Image,os,time,os.path,popen2,re,shutil
from optparse import OptionParser

class Conv:
    def __init__(self,fname,fpath):
        self.fname=fname
        self.fpath=fpath
        self.basedir=fpath
        self.outdir=fpath+'_conv'
        self.mp3=fpath+'.mp3'
        self.jpg_len=1.0
        self.smdir=fpath+'_smaller'
        self.lgdir=fpath+'_larger'
        self.pnum=[]
        self.duration=''
        self.fps=''

    def convfile(self,filename=''):
        basedir=self.basedir
        outdir=self.outdir
        R,G,B=0,1,2
        t1=time.time()
        im=Image.open(basedir+'/'+filename)
        im=im.convert('RGB')
        pxlist=list(im.getdata())
        pxlist2=list_sort(pxlist,len(pxlist))
    ##    pxlist.sort(lambda y,x:cmp(x[R]+x[G]+x[B],y[R]+y[G]+y[B]))
    ##    pxlist.reverse()
        out=Image.new(im.mode,im.size)
        out.putdata(pxlist2)
        out.save(outdir+'/'+filename)
        t1=(time.time()-t1)*1000
        (num,attr)=filename.split('.')
        num=int(num)
        sep=int(self.jpg_len/100)
        t=(filename,t1)
        self.pnum.append(t)
        if num % sep ==0 or num < sep:
            num=float(num)
            rate=(num/self.jpg_len)*100
            print 'total %d %.2f%% %s %d ms ok' % (self.jpg_len,rate,filename,t1)

    def get_duration_fps(self,std_err):
        line=[]
        l1=''
        duration=''
        fps=''
        for l in std_err.readlines():
            if not re.match('^\s\s',l):
                line.append(l1)
                l1=l.strip()
            else:
                l1=l1+l.strip()
        for l in line:
            if not re.match(r'^Input',l):
                continue
            m=re.search(r'Duration:\s+(\d+:\d+:\d+\.\d+)',l)
            if m:
                duration=m.group(1)
            m=re.search(r'(\d+\.\d+)\s+fps',l)
            if m:
                fps=m.group(1)
        print 'du=%s fps=%s' % (duration,fps)
        return duration,fps

    def pcheck(self):
        if not os.path.isdir(self.smdir):
            os.mkdir(self.smdir)
        if not os.path.isdir(self.lgdir):
            os.mkdir(self.lgdir)
        self.pnum.sort(lambda x,y:cmp(x[1],y[1]))
        min=int(len(self.pnum)*0.05)
        max=int(len(self.pnum)*0.95)
        min=self.pnum[:min]
        max=self.pnum[max:]
        for m in min:
            (f,t)=m
            src=self.basedir+'/'+f
            dst=self.smdir+'/'+f
            shutil.copy2(src,dst)
            print 'fname=%s time=%d ms' % (f,t)
        for m in max:
            (f,t)=m
            src=self.basedir+'/'+f
            dst=self.lgdir+'/'+f
            shutil.copy2(src,dst)
            print 'fname=%s time=%d ms' % (f,t)
    def fileop(self):
        basedir=self.basedir
        outdir=self.outdir
        fname=self.fname
        if not os.path.isdir(basedir):
            os.mkdir(basedir)
        if not os.path.isdir(outdir):
            os.mkdir(outdir)
        print fname
        command='ffmpeg -y -b 1000 -hq -i %s %s/%%5d.jpg' % (fname,basedir)
        (r,w,e)=popen2.popen3(command)
        (duration,fps)=self.get_duration_fps(e)
        list=os.listdir(basedir)
        self.jpg_len=len(list)
        for l in list:
           self.convfile(l)
        command='ffmpeg -y -t %s -r %s -b 1000 -hq -i %s/%%5d.jpg %s.mpg >/dev/null' % (duration,fps,outdir,outdir)
        print command
        os.system(command)
    def attachMP3(self):
        command='ffmpeg -y -vn -ab 64 -i %s %s >/dev/null' % (self.fname,self.mp3)
        os.system(command)
        if os.path.isfile(self.mp3):
            command='ffmpeg -y -t %s -r %s -b 1000 -hq -ab 64 -i %s.mpg -i %s %s_mp3.mpg >/dev/null' % (self.duration,self.fps,self.outdir,self.mp3,self.outdir)
            print command
            os.system(command)
        
    def cleanup(self):
        if os.path.isdir(self.basedir):
            command='rm -r %s' % (self.basedir)
            os.system(command)
        if os.path.isdir(self.outdir):
            command='rm -r %s' % (self.outdir)
            os.system(command)
        if os.path.isfile(self.mp3):
            command='rm %s' % self.mp3
            os.system(command)
    
def main():
    parser=OptionParser()
    parser.add_option("-i","--import",dest="importfile")
    (options,args)=parser.parse_args()
    if not options.importfile:
        print "usage -i finename"
        return
    fname=options.importfile
    if os.path.isfile(fname):
        (fpath,attr)=fname.split('.')
    else:
        print 'not exist this file'
    c=Conv(fname,fpath)
    c.fileop()
    c.pcheck()
    c.attachMP3()
    c.cleanup()

if __name__=='__main__':
    main()
