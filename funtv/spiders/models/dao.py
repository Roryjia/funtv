# -*- coding: utf-8 -*-

"""
Description
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import redis

__author__ = 'awang'

Base = declarative_base()


class Dao(object):
    """"""
    __db_uri = 'sqlite:///:memory:'  # 默认就是sqlite
    __echo = True
    __coding = 'utf8'
    __rds_host = '127.0.0.1'
    __rds_port = 18000
    __rds_db = 1
    __session = None
    __redis = None
    __connect = None
    __media_con = None

    @staticmethod
    def init_db_uri(env=None):
        if env == 'production':
            db_type = 'mysql'
            db_user = 'root'
            db_host = '192.168.0.3'
            db_password = '1qiding@mysql'
            db_name = 'yiqiding'
            rds_host = '127.0.0.1'
            rds_port = 18000
            rds_db = 1
            Dao.__echo = False
        elif env == 'test':
            db_type = 'mysql'
            db_user = 'root'
            db_host = '192.168.0.3'
            db_password = '1qiding@mysql'
            db_name = 'yiqidingtest'
            rds_host = '127.0.0.1'
            rds_port = 18000
            rds_db = 1
            Dao.__echo = False
        elif env == 'rory':
            db_type = 'mysql'
            db_user = 'root'
            db_host = '127.0.0.1'
            db_password = '123456'
            db_name = 'yiqidingtest'
            rds_host = '127.0.0.1'
            rds_port = 6379
            rds_db = 1
        else:
            db_type = 'mysql'
            db_user = 'root'
            db_host = '127.0.0.1'
            db_password = '123qwe'
            db_name = 'yqc'
            rds_host = '127.0.0.1'
            rds_port = 18000
            rds_db = 1
        Dao.__db_uri = '{}://{}:{}@{}/{}?charset=utf8'.format(
            db_type, db_user, db_password, db_host, db_name)
        Dao.__rds_host = rds_host
        Dao.__rds_port = rds_port
        Dao.__rds_db = rds_db

    @staticmethod
    def db_uri(user='root', host='127.0.0.1', password='123qwe', db='yqc'):
        return 'mysql://{}:{}@{}/{}?charset=utf8'.format(user, password, host, db)

    @staticmethod
    def engine():
        """"""
        return create_engine(Dao.__db_uri, echo=Dao.__echo, encoding=Dao.__coding)

    @staticmethod
    def media_engine(uri):
        """"""
        return create_engine(uri, echo=Dao.__echo, encoding=Dao.__coding)

    @staticmethod
    def db_session():
        """"""
        if Dao.__session is None:
            Dao.__session = Session(bind=Dao.engine())
        return Dao.__session

    @staticmethod
    def db_connect():
        """"""
        if Dao.__connect is None:
            Dao.__connect = Dao.engine().connect()
        return Dao.__connect

    @staticmethod
    def media_connect():
        """"""
        if Dao.__media_con is None:
            Dao.__media_con = Dao.media_engine(Dao.db_uri(
                user='root', host='192.168.0.3', password='1qiding@mysql', db='yiqiding_ktv'))
        return Dao.__media_con

    @staticmethod
    def init_schema():
        """"""
        Base.metadata.create_all(bind=Dao.engine())

    @staticmethod
    def rds():
        """"""
        if Dao.__redis is None:
            Dao.__redis = redis.Redis(
                connection_pool=redis.ConnectionPool(
                    host=Dao.__rds_host,
                    port=Dao.__rds_port,
                    db=Dao.__rds_db
                )
            )
        return Dao.__redis