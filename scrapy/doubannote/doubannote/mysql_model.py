#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy.types import CHAR, Integer, TIMESTAMP, Text
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()
# DB连接配置
DB_CONNECT_STRING = 'mysql+mysqldb://${user}:${passwd}@${hostname}:3306/scrapy'
engine = None
DB_Session = None


def init_db_session():
    global engine
    engine = create_engine(DB_CONNECT_STRING, echo=False)
    global DB_Session
    DB_Session = sessionmaker(bind=engine)


def get_session():
    return MySession()


class MySession(object):
    def __init__(self, *arg, **warg):
        if not DB_Session:
            init_db_session()
            BaseModel.metadata.create_all(engine)
        self.session = DB_Session()

    def __enter__(self):
        return self.session

    def __exit__(self, *arg, **warg):
        self.session.close()


# 数据表对应ORM模型
class DoubanNote(BaseModel):
    __tablename__ = 'doubannote'
    __table_args__ = {
        'mysql_engine': 'InnoDB'
    }

    url = Column(CHAR(255), primary_key=True)
    title = Column(CHAR(255))
    author = Column(CHAR(255))
    tags = Column(CHAR(255))
    snippet = Column(Text)
    comment_num = Column(Integer)
    pub_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
