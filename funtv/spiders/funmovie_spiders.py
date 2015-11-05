# -*-coding:utf-8 -*-
# 
# Copyright (C) 2012-2015 LuoHa TECH Co., Ltd. All rights reserved.
# Created on 2015-09-11, by rory
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

# from sqlalchemy import create_engine
#
# DB_URL = 'mysql://root:123456@127.0.0.1/yiqidingtest?charset=utf8'
#
# conn = create_engine(DB_URL, encoding='utf8')

from models.fun_video import FunVideo
from models.dao import Dao

# from utils.utils import get_funtv_mp4
from utils.pinyin import pinyin

Dao.init_db_uri('rory')
db_session = Dao.db_session()


class FunMovieSpider(CrawlSpider):
    """
    风行视频爬取
    """

    name = 'fun_movie'
    allows_domains = ['fun.tv', ]
    start_urls = [
        'http://www.fun.tv/retrieve/c-e794b5e5bdb1.n-e5bdb1e78987.o-pl.pg-1'
    ]

    # http://www.fun.tv/vplay/g-118135.v-635102/
    # http://www.fun.tv/vplay/g-64128/

    rules = [
        Rule(sle(allow=('/retrieve/c-e794b5e5bdb1.n-e5bdb1e78987.o-pl.pg-\d+$', )), follow=True, callback='parse1'),
        # Rule(sle(allow=('/retrieve/c-e794b5e5bdb1.n-e5bdb1e78987.o-pl.pg-\d+$', )), callback='parse1'),
        # Rule(sle(allow=('/vplay/g-\d+/?$', )), callback='parse2'),
    ]

    def parse1(self, response):

        sel = Selector(response)

        movie_list = sel.css('body div.mod-list.page-wrap div div.mod-wrap-in.mod-vd-lay-c6.fix div.mod-vd-i')
        for movie in movie_list:
            movie_id = movie.css('div.info h3 a::attr(data-id)').extract()[0]

            if db_session.query(FunVideo).filter(FunVideo.id == movie_id).first():
                continue

            name = movie.css('div.info h3 a::attr(title)').extract()[0]
            image = movie.css('div.pic a img::attr(_lazysrc)').extract()[0]
            description = movie.css('div.info p::text').extract()[0]
            point = movie.css('div.info h3 b::text').extract()[0]

            request = Request('http://www.fun.tv{}'.format(movie.css('div.pic a::attr(href)').extract()[0]), callback=self.parse2)
            fv = FunVideo(id=movie_id, name=name, name_pinyin=pinyin.get_initials(name, splitter=''),
                          image=image, description=description, point=point)

            request.meta['movie'] = fv
            yield request

    def parse2(self, response):
        movie = response.meta['movie']

        sel = Selector(response)
        origin_url = response.url
        director = ''.join(sel.css('div#main-rt div.mod-datum p:nth-child(2) span::text').extract())
        starring = ''.join(sel.css('div#main-rt div.mod-datum p:nth-child(3) span::text').extract())
        detail = sel.css('div#main-rt div.mod-datum p.dirtext span:nth-child(2)::text').extract()[0]
        category = ''.join(sel.css('div#main-rt div.mod-datum p:nth-child(4) span::text').extract())
        play_count = sel.css('div.playInfo.crumbs div.rightBtn.fix a::text').extract()[0]

        print movie.name, '------->', origin_url, '------->', play_count

        if play_count:
            play_count = ''.join(play_count[3:].split(','))

            movie.origin_url = origin_url
            movie.director = director
            movie.starring = starring
            movie.detail = detail
            movie.category = category
            movie.play_count = play_count

            # if movie.play_count.strip() not in [0, '0']:
            #     for f in ['fluent', 'normal', 'high', 'super']:
            #         mp4_url = get_funtv_mp4(origin_url, f)
            #         if mp4_url:
            #             column_name = 'mp4_url_{}'.format(f)
            #             setattr(movie, column_name, mp4_url)
            #             movie.enable = 1

            db_session.add(movie)
            db_session.commit()