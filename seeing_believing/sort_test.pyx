cdef extern from "Python.h":
    void* PyMem_Malloc(int n) except NULL
    void* PyMem_Realloc(void *p, int n) except NULL
    void  PyMem_Free(void *p)
    object PyString_FromStringAndSize(char *, int)
    int PyObject_AsReadBuffer(object obj, void **buffer, int
    *buffer_len) except -1
    int PyObject_Compare(object o1, object o2) except *

cdef extern from "string.h":
    void* memmove(void *DST, void *SRC, int LENGTH)

cdef struct rgbt:
    int r
    int g
    int b
    float l

def list_sort(data,size):
    cdef int si
    si=size
    cdef rgbt *lst
    cdef rgbt temp
    cdef rgbt *result
    ret=[]
    lst=<rgbt *>PyMem_Malloc(sizeof(rgbt)*si)
    for i from 0 <= i <si:
        lst[i].r=data[i][0]
        lst[i].g=data[i][1]
        lst[i].b=data[i][2]
        lst[i].l=0.298912*lst[i].r+0.586611*lst[i].g+0.114478*lst[i].b
##luminance = ( 0.298912 * r + 0.586611 * g + 0.114478 * b );
    result=qsort_entry(lst,si)
    
    for i from 0<=i <si:
        rgb=(lst[i].r,lst[i].g,lst[i].b)
        ret.append(rgb)
    PyMem_Free(lst)
    return ret

cdef rgbt* sort(rgbt *d1,int size):
    cdef unsigned int i,j,k
    cdef rgbt temp
    for i from 0 <=i < size-1:
        k=i
        for j from i+1 <= j <size:
            if(d1[k].l>d1[j].l):
                k=j
        temp=d1[i]
        d1[i]=d1[k]
        d1[k]=temp
    return d1     

cdef rgbt* bubble_sort(rgbt *d1,int size):
     cdef unsigned int i,j
     cdef rgbt temp
     for i from 0 <= i <size:
          for j from size-1 >= j > i:
            if(d1[j-1].l>d1[j].l):
                temp=d1[j-1]
                d1[j-1]=d1[j]
                d1[j]=temp
     return d1
cdef rgbt* qsort_entry(rgbt *d1,int size):
    qsort(0,d1,size-1)
    return d1

cdef void qsort(int left,rgbt *d1,int right):
    cdef int i,j
    cdef rgbt temp
    if(left >= right):
        return
    j=left
    for i from left+1 <= i <= right:
        if(d1[i].l < d1[left].l):
            j=j+1
            temp=d1[j]
            d1[j]=d1[i]
            d1[i]=temp
    temp=d1[left]
    d1[left]=d1[j]
    d1[j]=temp
##    print 'left=%d,right=%d,i=%d,j=%d' % (left,right,i,j)
    qsort(left,d1,j-1)
    qsort(j+1,d1,right)