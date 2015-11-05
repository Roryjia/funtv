# -*-coding:utf-8 -*-
# 
# Copyright (C) 2012-2015 LuoHa TECH Co., Ltd. All rights reserved.
# Created on 2015-09-11, by rory
# 
# 

__author__ = 'rory'


import requests

from bs4 import BeautifulSoup

def get_funtv_mp4(url, format):

    URL = 'http://www.flvcd.com/parse.php'
    PARAMS = {
        'kw': url,
        'flag': 'one',
        'format': format,
    }

    headers = {
        'Referer': 'http://www.flvcd.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
    }

    try:
        res = requests.get(URL, params=PARAMS, headers=headers)
        html = res.content.decode('gbk')
        soup = BeautifulSoup(html)
        a = soup.find('a', attrs={'class': 'link'})
        return a.attrs.get('href', '')
    except Exception, e:
        print u'请求MP4 URL 报错:', e
        return ''


if __name__ == '__main__':
    mp4_url = get_funtv_mp4('http://www.fun.tv/vplay/g-201488/', 'fluent')
    print mp4_url
