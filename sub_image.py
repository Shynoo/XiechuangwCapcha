#!/usr/bin/env python
#coding:utf-8
import os,sys
from PIL import Image,ImageEnhance,ImageFont,ImageDraw,ImageFilter
from binary_process import horl_cut,perp_cut
import cv2
import numpy as np
from matplotlib import pyplot as plt

host_path="/Users/dengshougang/Downloads/VerifyImages/工商局67"

def load_img(n,path="processed",suffix='rotate_result2', n2='0'):
    return Image.open(host_path+"/"+path+"/"+str(n)+"/"+suffix+n2+".png")

def store_img(image,n,suffix="sub",n2=''):
    try:
        os.mkdir(host_path+"/sub")
    except OSError:
        pass
    try:
        os.mkdir(host_path + "/sub/" + str(n))
    except OSError:
        pass
    image.save(host_path+"/sub/"+str(n)+"/"+suffix+str(n2)+".png")

def image_mid(image):
    im = image
    width = im.size[0]
    height = im.size[1]
    pix=im.load()
    xcross=[]
    for x in width:
        xcross.append(0)
        for y in height:
            r,g,b=pix[x,y]
            if r+g+b==0:
                xcross+=1


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
    box=()
    temp=0
    if diff % 2==1:
        temp=1
    if width>height:
        box=(diff/2,0,width-(diff/2)-temp,height)
    elif width<height:
        box=(0,diff/2,width,height-(diff/2)-temp)
    print box
    im2=im2.crop(box)
    im2.thumbnail((16,16))
    return im2

# def is_equarment(ls):


def move(frm="rotated",to="result0/all",n='0'):
    try:
        # os.mkdir(host_path+"/%s"%frm)
        pass
    except :
        pass
    try:
        os.mkdir(host_path + "/%s" % (to))
    except:
        pass
    ls=os.listdir(host_path+"/%s"%(frm))
    for dic in ls:
        l2 = os.listdir(host_path + "/%s/%s" % (frm, dic))
        mid=0
        for png in l2:
            if str(png).find("ate_result2")>1:
                mid+=1
        if mid==5:
            for png in l2:
                if str(png).find("ate_result2")>1:
                    with open(host_path+"/%s/%s/%s"%(frm,dic,png)) as src,open(host_path + "/%s/%s%s" % (to,dic,str(png)),"w") as des:
                        des.write(src.read())

def is_path_eqs(perfix="processed",n=0,suffix="rotate_result2"):
    f=open(host_path+"/"+perfix)

def convert_csv(image):
    im = image
    width = im.size[0]
    height = im.size[1]
    pix = im.load()
    xy=[]
    str=''
    for x in range(width):
        xy.append([])
        for y in range(height):
            xy[x].append(0)
            r, g, b = pix[x, y]
            xy[x][y]=r+g+b
            if r+g+b>127:
                str+='1'
            else:
                str+='0'
    with open(im.filename.replace("png","txt"),"wr") as cs:
        cs.write(str)
        print "store csv: %s"%cs.name

def convetall(path="result0"):
    ls=os.listdir(host_path+"/"+path)
    for ds in ls:
        dp=os.listdir(host_path+"/%s/%s"%(path,ds))
        for im in dp:
            if im.endswith("png"):
                convert_csv(Image.open(host_path+"/%s/%s/%s"%(path,ds,im)))


if __name__=="__main__":
    # im=load_img(0)
    # im2=sub_process(im)
    # convert_csv(Image.open("/Users/dengshougang/Downloads/VerifyImages/result0/0/34rotate_result20.png"))
    convetall()
    print
