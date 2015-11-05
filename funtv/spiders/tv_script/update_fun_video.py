# -*-coding:utf-8 -*-
# 
# Copyright (C) 2012-2015 LuoHa TECH Co., Ltd. All rights reserved.
# Created on 2015-09-15, by rory
# 
# 

__author__ = 'rory'

type = None

while 1:

    type = raw_input(u'请输入要解析的视频类型：\n'
                     u'0--------电影\n'
                     u'1--------电视\n'
                     u'2--------动画\n'
                     u'3--------综艺\n'.encode('utf8'))
    if type not in ['0','1', '2', '3']:
        continue

    break

headers = {
    "Accept": "application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
    "Accept-Charset": "GBK,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding": "gzip",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Cache-Control": "max-age=0",
    # "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.106 Safari/535.2",
}

import re

import random

import requests

session = requests.session()

from sqlalchemy import create_engine

FUN_TV_API = 'http://api.funshion.com/ajax/vod_panel/{}/w-1/'
FUN_TV_TOKEN_API = 'http://api.funshion.com/ajax/get_webplayinfo/{}/{}/mp4?user=funshion'
FUN_TV_SOURCE_API = 'http://jobsfe.funshion.com/query/v1/mp4/{}.json?clifz=fun&mac=&tm=1395365896&token={}'

DB_URL = 'mysql://root:123456@127.0.0.1/yiqidingtest?charset=utf8'
TEST_DB_URL = 'mysql://root:1qiding@mysql@192.168.0.3/yiqidingtest?charset=utf8'

conn = create_engine(DB_URL, encoding='utf8', echo=True).connect()

result = conn.execute("select id, name from fun_tv_video where `type`=%s and enable=0 ORDER BY id DESC ", type)

for m in result:
    print u'开始解析===========>{}'.format(m[1])
    mediaid = m[0]

    try:
        res = session.get(FUN_TV_API.format(mediaid), headers=headers, timeout=5).json()
    except Exception, e:
        print u'第一步请求出错', e
        continue

    if res.get('status') == 200:
        minfo = res.get('data').get('minfo')

        name = minfo.get('name_cn')
        number = minfo.get('torrentnum')
        conn.execute("update fun_tv_video set number={} where `id`={}".format(number, mediaid))

        fsps = res.get('data').get('fsps')

        for mult in fsps.get('mult'):
            serialid = mult.get('serialid')
            index = mult.get('number')

            image = mult.get('imagepath', '')
            description = mult.get('description', '')

            print u'开始解析:{}=====>第{}集'.format(name, index)

            if not conn.execute("select `id` from `sub_fun_tv_video` where `id` = {}".format(serialid)).first():
                conn.execute("insert into `sub_fun_tv_video`(id, fv_id, origin_url, `index`, play_count) "
                             "VALUES ('{}', '{}', '{}', '{}', '{}')".format(serialid, mediaid,
                                                                  'http://www.fun.tv{}'.format(mult.get('url', '')),
                                                                  index, 100
                                                                  ))

            db_sub_tv = conn.execute("select `mp4_url_fluent`, `mp4_url_normal`, `mp4_url_high`, `mp4_url_super` from `sub_fun_tv_video` where `id` = {}".format(serialid)).first()

            if all(db_sub_tv.values()):
                continue

            try:
                res1 = session.get(FUN_TV_TOKEN_API.format(mediaid, index), headers=headers, timeout=5).json()
            except Exception, e:
                print u'第二步请求出错', e
                continue

            token = res1.get('token')

            clarity = {
                'high-dvd': '',
                'dvd': '',
                'tv': '',
                'super-dvd': '',
            }

            for fs in res1.get('fsps'):

                if fs.get('url') and not clarity.get(fs.get('clarity')):

                    print u'开始解析清晰模式-->{}'.format(fs.get('clarity'))

                    hashid = re.findall(r"fsp://(\w+)", fs.get('url'))[0]

                    try:
                        res2 = session.get(FUN_TV_SOURCE_API.format(hashid, token), headers=headers, timeout=5).json()
                    except Exception:
                        clarity[fs.get('clarity')] = ''
                    else:
                        if res2.get('playlist'):
                            urls = res2.get('playlist')[0].get('urls')
                            clarity[fs.get('clarity')] = urls[random.randint(0, len(urls)-1)]

            print clarity

            conn.execute(u'''update `sub_fun_tv_video` set mp4_url_fluent="{}", mp4_url_normal="{}",'''
                         u'''mp4_url_high="{}", mp4_url_super="{}", `index`={}, `image`="{}", `description`='{}' where `id`={}'''.
                         format(clarity.get('tv', ''), clarity.get('dvd', ''), clarity.get('high-dvd', ''), clarity.get('super-dvd', ''), index, image, description, serialid))

        conn.execute("update fun_tv_video set enable=1 where `id`={}".format(mediaid))

