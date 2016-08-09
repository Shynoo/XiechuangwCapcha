#!/usr/bin/env python
#coding:utf-8
import os,sys,time
# from math import atan2,pi,sqrt
# import cPickle as pickle
from PIL import Image,ImageEnhance,ImageFont,ImageDraw,ImageFilter
# import cv2
# import numpy as np
# from matplotlib import pyplot as plt

"""
    对"http://www.xiechuangw.com/shenzhen/"
    深圳工商局网站验证码的识别,等式类成功率60%,非等式类直接跳过
"""

def sub_process(image):
    im=image
    im2=im.copy()
    im2=horl_cut(im2)
    im2=perp_cut(im2)
    width = im2.size[0]
    height = im2.size[1]
    im2=im2.crop((1,1,width,height))
    # if width>20:
    #     im2=im2.crop((2,0,width-2,height))
    # if height>20:
    #     im2=im2.crop((0,2,im2.size[0],height-2))
    width = im2.size[0]
    height = im2.size[1]
    diff=abs(width-height)
    if diff==0:
        im2.resize((24, 24))
        return im2
    box=()
    temp=0
    if diff % 2==1:
        temp=1
    if width>height:
        box=(diff/2,0,width-(diff/2)-temp,height)
    elif width<height:
        box=(0,diff/2,width,height-(diff/2)-temp)
    # print box
    if box==(0,0,0,0):
        im2.resize((24, 24))
        return im2
    im2=im2.crop(box)
    im2=im2.resize((24,24))
    return im2

def load_img(n, suffix='verify', n2=''):
    return Image.open(host_path+"/origin/"+str(n)+"/"+suffix+n2+".png")

def store_img(image,n,path="trained",suffix="rotate_result",n2=''):
    try:
        os.mkdir(host_path+"/"+path)
    except OSError:
        pass
    try:
        os.mkdir(host_path + "/%s/%s/"%(path,str(n)))
    except OSError:
        pass
    image.save(host_path+"/"+path+"/"+str(n)+"/"+str(suffix)+str(n2)+".png")

def binary_and_split(image, begin=110, end=360):
    ls=[]
    for i in  range(begin,end):
        im=binary(image.copy(),i,i)
        if black_num(im)>=10 and (is_effctive(im)>0):
            ls.append(im)
    return ls

def cross_split(images):
     ls=[]
     xnum=[]
     if isinstance(images, list):
     # if 1:
         for im in images:
             pix=im.load()
             max5=0
             pointx=0
             width = im.size[0]
             height = im.size[1]
             xCross=[]
             for x in range(width):
                 xCross.append(0)
                 for y in range(height):
                     r,g,b= pix[x,y]
                     if r+g+b==0:
                         xCross[x]+=1
             for i in range(0,width):
                j=i
                temp=0
                while(j<i+5 and j<width):
                    temp += xCross[j]
                    j+=1
                if (temp > max5):
                    max5=temp
                    pointx=i
             begin = pointx
             end = pointx
             while begin>=2 and xCross[begin]>0 and xCross[begin-1]>0 and xCross[begin-2]>0:
                 begin-=1
             while end<width-2 and xCross[end]>0 and xCross[end+1]>0 and xCross[end+2]>0:
                 end+=1
             if abs(begin-end)<=8:
                 continue
             if begin >= 2 :
                 begin -=2
             if end < width-2:
                 end+=2
             ls.append([im.crop((begin,0,end,height)),pointx])
             xnum.append(pointx)
     def cmp(x, y):
         x2=x[1]
         y2=y[1]
         if x2<y2:
             return -1
         else:
             return 1
     ls.sort(cmp)
     lss=[]
     for ims in ls:
         lss.append(ims[0])
     return lss

def binary(im, begin=110, end=360):
    pix = im.load()
    width = im.size[0]
    height = im.size[1]
    for x in range(width):
        for y in range(height):
            r, g, b = pix[x, y]
            if(r+g+b>=begin and r+g+b<=end):
                pix[x,y]=(0,0,0)
            else:
                pix[x,y]=(255,255,255)
    return im

def black_num(image):
    sum=0
    im=image
    pix = im.load()
    width = im.size[0]
    height = im.size[1]
    for x in range(width):
        for y in range(height):
            r, g, b = pix[x, y]
            if (r+g+b==0):
                sum+=1
    return sum

def is_effctive(image,limit=2):
    im=image
    pix = im.load()
    width = im.size[0]
    height = im.size[1]
    max=0
    for x in range(0,width):
        temp=0
        for y in range(0,height):
            r,g,b=pix[x,y]
            # print r,g,b
            if r+g+b==0:
                temp+=1
        if temp>limit:
            return 1
    return 0

def horl_cut(image):
    im=image
    pix = im.load()
    width = im.size[0]
    height = im.size[1]
    sum=[]
    begin=0
    end=height
    for y in range(height):
        sum.append(0)
        for x in range(width):
            r, g, b = pix[x, y]
            if(r+g+b!=0):
                sum[y]+=1
                break
        if sum[y]==0:
            if y<20 and begin<y:
                begin=y
            elif y>=20 and end>y:
                end=y
    box=(0,begin,width,end)
    im=im.crop(box)
    if begin==end:
        return
    return im

def perp_cut(image):
    im=image
    pix = im.load()
    width = im.size[0]
    height = im.size[1]
    sum = []
    begin = 0
    end = width
    for x in range(width):
        sum.append(0)
        for y in range(height):
            r, g, b = pix[x, y]
            if (r+g+b!= 0):
                sum[x] += 1
        if sum[x] == 0:
            if x < width/2 and begin < x:
                begin = x
            elif x >= width/2 and end > x:
                end = x
    box = (begin,0, end,height )
    im= im.crop(box)
    return im

def revBlackWhite(image):
    im=image
    pix = im.load()
    width = im.size[0]
    height = im.size[1]
    for x in range(width):
        for y in range(height):
            r, g, b = pix[x, y]
            if (r + g + b == 0):
                pix[x, y] = (255, 255, 255)
            else:
                pix[x, y] = (0, 0, 0)
    return im

def rotate_process(image,n=0,n2='',bl=Image.BILINEAR):

    m = -30
    maxdiff=0
    arc=0
    while m <= 30:
        im = image.copy()
        m2= test_rotate(im,m,bl)
        if m2>maxdiff:
            maxdiff=m2
            arc=m
        m += 1
    im=image.rotate(arc,bl,expand=1)
    im = horl_cut(im)
    im = perp_cut(im)

    return im

def test_rotate(image, arc, bl=Image.BICUBIC):
    im=image
    im=im.rotate(arc, bl, expand=1)
    im=horl_cut(im)
    im=perp_cut(im)
    pix = im.load()
    width = im.size[0]
    height = im.size[1]
    ycross = []
    ydiff=[]
    diffsum=0
    for y in range(0, height):
        ycross.append(0)
        ydiff.append(0)
        for x in range(0, width):
            r, g, b = pix[x, y]
            if r + g + b != 0:
                ycross[y] += 1
    for y in range(1, height):
        ydiff[y]=ycross[y]-ycross[y-1]
        diffsum+=abs(ydiff[y])
    # print arc,diffsum
    return diffsum

def process(begin,end):
    for i in range(begin,end+1):
        n = i
        img = load_img(n)
        im = img.copy()
        ls = binary_and_split(im)
        ls = cross_split(ls)
        idd = 0
        for im in ls:
            horl_cut(im)
            perp_cut(im)
            revBlackWhite(im)
            horl_cut(im)
            perp_cut(im)
            bl=Image.BILINEAR
            im2=rotate_process(im, n, n2=idd,bl=bl)
            im2=sub_process(im2)
            store_img(im2, n, suffix="rotate_result" + str(bl)[0:8],n2=idd)
            idd += 1
        print img.filename," processed"

def split_img(img):
    im = img.copy()
    ls = binary_and_split(im)
    ls = removeString(ls,7)
    ls = cross_split(ls)
    return ls

def compare(s1,s2):
    m=0
    for i in range(len(s1)):
        if s1[i]==s2[i]:
            m+=1
    return m

def feature(image):
    im = image
    width = im.size[0]
    height = im.size[1]
    pix = im.load()
    xy = []
    str=''
    for x in range(width):
        xy.append([])
        for y in range(height):
            xy[x].append(0)
            r, g, b = pix[x, y]
            xy[x][y] = r + g + b
            if r + g + b > 127:
                str += '1'
            else:
                str += '0'
    return  str

def verify(str,idd):
    path=host_path+"/result0"
    ls=os.listdir(path)
    max=0
    code=''
    for cd in ls:
            if idd==0 or idd==2:
                if len(cd)!=1:
                    continue
            else:
                if len(cd)==1:
                    continue
            fs=os.listdir(path+"/"+cd)
            for fil in fs:
                if fil.endswith(".txt"):
                    with open(path+"/%s/%s"%(cd,fil)) as f:
                        st=f.readline()
                        po=compare(st,str)
                        if po >max:
                            max=po
                            code=cd
    return code

def caculate(ls):
    if ls[1]=='add':
        return int(ls[0])+int(ls[2])
    elif ls[1]=='sub':
        return int(ls[0])-int(ls[2])
    else:
        return int(ls[0])*int(ls[2])


def identify(ls):
    if isinstance(ls,list):
        re=[]
        idd=0
        for im in ls[0:3]:
            horl_cut(im)
            perp_cut(im)
            revBlackWhite(im)
            horl_cut(im)
            perp_cut(im)
            bl = Image.BILINEAR
            im2 = rotate_process(im, bl=bl)
            im2 = sub_process(im2)
            str=feature(im2)
            ver=verify(str,idd)
            idd+=1
            re.append(ver)
            store_img(im2,ver,"trained1",time.time())
    return re

host_path="/Users/dengshougang/Downloads/VerifyImages/工商局67"

def procs(begin,end):
    path=host_path+"/download"
    allbe=time.time()
    for n in range(begin,end+1):
        begint = time.time()
        img=Image.open(path+"/"+str(n)+"/verify.png")
        ls=split_img(img)
        print n,
        if len(ls)==5:
            re=identify(ls)
            print re,
            m=caculate(re)
            print m,
        print
        print "cost time:", str(time.time() - begint)
        print "all cost time", str(time.time()-allbe)

def removeString(ls,limit=7):
    for im in ls:
        pix=im.load()
        r,g,b=pix[0,0]
        # if r+g+b>700:
        for x in xrange(1,im.width-1,1):
            for y in xrange(1,im.height-1,1):
                mid = 0
                r, g, b = pix[x - 1, y - 1]
                if r + g + b > 700:
                    mid += 1
                r, g, b = pix[x - 1, y ]
                if r + g + b > 700:
                    mid += 1
                r, g, b = pix[x - 1, y + 1]
                if r + g + b > 700:
                    mid += 1
                r, g, b = pix[x +1, y - 1]
                if r + g + b > 700:
                    mid += 1
                r, g, b = pix[x + 1, y ]
                if r + g + b > 700:
                    mid += 1
                r, g, b = pix[x+1, y+1]
                if r + g + b > 700:
                    mid += 1
                r, g, b = pix[x, y - 1]
                if r + g + b > 700:
                    mid += 1
                r, g, b = pix[x, y + 1]
                if r + g + b > 700:
                    mid += 1
                if mid>=limit:
                    pix[x,y]=(255,255,255)
    return ls


def idiomProcess(begin,end):
    path=host_path+"/download"
    for n in range(begin,end+1):
        img=Image.open(path+"/"+str(n)+"/verify.png")
        ls=split_img(img)
        idd=0
        for im in ls:
            store_img(im,n=n,path="split",suffix="split",n2=idd)
            idd+=1


if __name__=="__main__":
    idiomProcess(0,10)
