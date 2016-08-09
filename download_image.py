#!/usr/bin/env python
# coding:utf-8
import requests
from PIL import Image
from io import StringIO
from tqdm import tqdm
import os
import time
import math
from random import random


url="http://www.szcredit.com.cn/web/WebPages/Member/CheckCode.aspx?"
headers = {
              "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
              "Accept-Encoding": "gzip, deflate, sdch",
              "Connection": "keep-alive",
              "Cache-Control": "max-age=0",
              # "Cookie": "gsScrollPos=; PHPSESSID=baphcsk4q44o9esl19dsb1rso7",
              "Upgrade-Insecure-Requests": "1",

              # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
              "Accept-Language": "zh-CN,zh;q=0.8",
              "Content-Type": "application/json",
              "DNT": "1",
          }

def download(path,begin,end):
    try:
        os.mkdir(path)
    except:
        pass
    for n in range(begin,end+1):
        try:
            os.mkdir(path+"/"+str(n))
        except:
            pass
        response = requests.get(url+str(random()), headers,stream=True)
        with open(path +"/"+ str(n)+"/verify.png", "wb") as f:
            for data in tqdm(response.iter_content()):
                f.write(data)
            print f.name
        time.sleep(0.5)


if __name__=="__main__":
    store_path="/Users/dengshougang/Downloads/VerifyImages/深圳信用网/download"
    download(store_path,1001,2000)
