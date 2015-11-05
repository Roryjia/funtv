# -*-coding:utf-8 -*-
# 
# Copyright (C) 2012-2015 LuoHa TECH Co., Ltd. All rights reserved.
# Created on 2015-09-13, by rory
# 
# 

__author__ = 'rory'


from scrapy import Request
from scrapy.selector import Selector

try:
    from scrapy.spider import Spider
except ImportError, e:
    from scrapy.spider import BaseSpider as Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle

from models.fun_video import FunVideo, SubFunViedo
from models.dao import Dao

from utils.pinyin import pinyin

Dao.__echo = False
Dao.init_db_uri('rory')
Dao.init_schema()
db_session = Dao.db_session()


class FunTVSpider(CrawlSpider):
    """
    风行电视爬取
    """

    name = 'fun_tv'
    allows_domains = ['fun.tv', ]
    start_urls = [
        'http://www.fun.tv/retrieve/c-e794b5e8a786e589a7.n-e5bdb1e78987.pg-1'
    ]

    rules = [
        Rule(sle(allow=('/retrieve/c-e794b5e8a786e589a7.n-e5bdb1e78987.pg-\d+$', )), follow=True, callback='parse1'),
    ]

    def parse1(self, response):
        sel = Selector(response)

        tv_list = sel.css('body div.mod-list.page-wrap div div.mod-wrap-in.mod-vd-lay.fix div.mod-vd-i')

        for tv in tv_list:
            tv_id = tv.css('div.info h3 a::attr(data-id)').extract()[0]

            if db_session.query(FunVideo).filter(FunVideo.id == tv_id).first():
                continue

            name = tv.css('div.info h3 a::attr(title)').extract()[0]
            image = tv.css('div.pic a img::attr(_lazysrc)').extract()[0]
            description = tv.css('div.info p::text').extract()[0]
            point = tv.css('div.info h3 b::text').extract()[0]

            request = Request('http://www.fun.tv{}'.format(tv.css('div.pic a::attr(href)').extract()[0]), callback=self.parse2)
            fv = FunVideo(id=tv_id, name=name, name_pinyin=pinyin.get_initials(name, splitter=''),
                          image=image, description=description, point=point)

            request.meta['tv'] = fv
            yield request

    def parse2(self, response):
        tv = response.meta['tv']

        sel = Selector(response)
        tv.origin_url = response.url
        tv.director = ''.join(sel.css('div#main-rt div.mod-datum p:nth-child(2) span::text').extract())
        tv.starring = ''.join(sel.css('div#main-rt div.mod-datum p:nth-child(3) span::text').extract())
        tv.category = ''.join(sel.css('div#main-rt div.mod-datum p:nth-child(4) span::text').extract())

        tv.detail = sel.css('div#main-rt div.mod-datum p.dirtext span:nth-child(2)::text').extract()[0]

        print tv.name, '------->', tv.origin_url

        # 表明电视
        tv.type = 1

        db_session.add(tv)
        db_session.commit()

        sub_tv_list = sel.css('div#playCont div div div div.torrent-panel ul li')

        for st in sub_tv_list:
            try:
                st.css('a span').extract()[0]
            except IndexError:
                sub_tv_index = st.css('::attr(data-idx)').extract()[0]
            else:
                continue

            sub_tv = SubFunViedo(fv_id=tv.id, index=sub_tv_index)
            sub_tv.id = st.css('::attr(data-vid)').extract()[0]
            sub_tv.origin_url = 'http://www.fun.tv{}'.format(st.css('a::attr(href)').extract()[0])

            print sub_tv.index, '-------->', sub_tv.origin_url

            request1 = Request(sub_tv.origin_url, callback=self.parse3)
            request1.meta['sub_tv'] = sub_tv
            yield request1

    def parse3(self, response):

        print 'parse 3 ------->'

        sub_tv = response.meta['sub_tv']

        sel = Selector(response)
        play_count = sel.css('div.playInfo.crumbs div.rightBtn.fix a::text').extract()[0]

        sub_tv.play_count = ''.join(play_count[3:].split(','))

        db_session.add(sub_tv)
        db_session.commit()