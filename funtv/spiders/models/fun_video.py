# -*- coding: utf-8 -*-

"""
Description
"""

__author__ = 'TT'

from sqlalchemy import Column, String, Integer, Text, Float
from dao import Base
import time


class FunVideo(Base):
    """"""
    __tablename__ = 'fun_tv_video'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), default='')
    name_pinyin = Column(String(200), default='')
    origin_url = Column(String(200), default='')

    mp4_url_fluent = Column(String(200), default='', doc=u'流畅')
    mp4_url_normal = Column(String(200), default='', doc=u'标清')
    mp4_url_high = Column(String(200), default='', doc=u'高清')
    mp4_url_super = Column(String(200), default='', doc=u'超清')

    image = Column(String(200), default='')
    description = Column(Text, default='')
    point = Column(Float, default=0)
    play_count = Column(Integer, default=0)
    order_no = Column(Integer, default=0)
    director = Column(String(200), default='')
    starring = Column(String(300), default='')
    detail = Column(Text, default='')

    style = Column(Integer, default=0)
    type = Column(Integer, default=0, doc=u'0--电影, 1--电视, 2--动画, 3--综艺')
    number = Column(Integer, default=1, doc=u'影视集数')

    category = Column(String(100), default='')
    enable = Column(Integer, default=0)
    create_at = Column(Integer, default=lambda: int(time.time()))


class SubFunViedo(Base):
    """
    电视/动漫 分集
    """
    __tablename__ = 'sub_fun_tv_video'

    id = Column(Integer, primary_key=True)

    play_count = Column(Integer, default=0)

    fv_id = Column(Integer, doc=u'电视ID')
    index = Column(Integer, default=0)

    image = Column(String(200), default='')
    description = Column(Text, default='')

    origin_url = Column(String(200), default='')

    mp4_url_fluent = Column(String(200), default='', doc=u'流畅')
    mp4_url_normal = Column(String(200), default='', doc=u'标清')
    mp4_url_high = Column(String(200), default='', doc=u'高清')
    mp4_url_super = Column(String(200), default='', doc=u'超清')