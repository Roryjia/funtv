# -*-coding:utf-8 -*-
# 
# Copyright (C) 2012-2015 LuoHa TECH Co., Ltd. All rights reserved.
# Created on 2015-09-17, by rory
# 
# 

__author__ = 'rory'

import time
import random
import math

def createSid():
    nowTime = int(time.time() *1000)
    random1 = random.randint(1000,1998)
    random2 = random.randint(1000,9999)
    return "%d%d%d" %(nowTime,random1,random2)

def getFileIDMixString(seed):
    mixed=[]
    source=list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\:._-1234567890")
    seed=float(seed)
    for i in range(len(source)):
        seed = (seed * 211 + 30031 ) % 65536
        index = math.floor(seed /65536 *len(source))
        mixed.append(source[int(index)])
        source.remove(source[int(index)])
    return mixed

def getFileId(fileId,seed):
    mixed=getFileIDMixString(seed)
    ids=fileId.split('*')
    realId=[]
    for ch in ids:
        realId.append(mixed[int(ch)])
    return ''.join(realId)

if __name__ == '__main__':
    print createSid()
    fileId='65*53*65*65*65*50*40*18*65*65*18*18*40*25*3*50*60*50*46*31*46*60*65*18*51*13*65*46*31*31*42*18*50*53*51*13*60*40*59*12*53*50*57*59*31*12*66*25*59*60*65*25*42*59*50*66*42*46*66*40*42*46*12*65*13*12'
    seed=566
    print getFileId(fileId,seed)