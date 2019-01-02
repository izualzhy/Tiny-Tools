# -*- coding: utf-8 -*-

from mysql_model import get_session, DoubanNote

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DoubannotePipeline(object):
    def process_item(self, item, spider):
        douban_note = DoubanNote()
        douban_note.url = item['url']
        douban_note.author = item['author']
        douban_note.title = item['title']
        douban_note.pub_date = item['pub_date']
        douban_note.snippet = item['snippet']
        douban_note.comment_num = item['comment_num']
        douban_note.tags = item['tags']
        with get_session() as session:
            session.merge(douban_note)
            session.commit()
        return item
