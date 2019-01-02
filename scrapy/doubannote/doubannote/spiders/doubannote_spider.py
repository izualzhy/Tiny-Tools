#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from doubannote.items import DoubannoteItem


class DoubannoteSpider(scrapy.Spider):
    name = 'Doubannote'
    allowed_domains = ['douban.com']
    start_urls = [
        'https://www.douban.com',
        'https://www.douban.com/explore/',
        'https://www.douban.com/explore/column/10',
        'https://www.douban.com/explore/column/17',
        'https://www.douban.com/explore/column/13',
        'https://www.douban.com/explore/column/7',
        'https://www.douban.com/explore/column/2',
        'https://www.douban.com/explore/column/12',
        'https://www.douban.com/explore/column/18',
        'https://www.douban.com/explore/column/11',
        'https://www.douban.com/explore/column/8',
        'https://www.douban.com/explore/column/4',
        'https://www.douban.com/explore/column/14',
        'https://www.douban.com/explore/column/24',
        'https://www.douban.com/explore/column/19',
        'https://www.douban.com/explore/column/6',
        'https://www.douban.com/explore/column/25',
        'https://www.douban.com/explore/column/23',
        'https://www.douban.com/explore/column/3',
        'https://www.douban.com/explore/column/20',
        'https://www.douban.com/explore/column/16',
        'https://www.douban.com/explore/column/1041',
        'https://www.douban.com/explore/column/9',
        'https://www.douban.com/explore/column/15',
        'https://www.douban.com/explore/column/27',
        'https://www.douban.com/explore/column/1029'
    ]

    def parse(self, response):
        sel = scrapy.Selector(response)

        if response.url.startswith('https://www.douban.com/note'):
            doubannote_item = DoubannoteItem()
            doubannote_item['url'] = response.url
            doubannote_item['title'] = \
                sel.xpath('//*[@class="note-header note-header-container"]/h1/text()').\
                extract()[0].encode('utf8')
            doubannote_item['author'] = \
                sel.xpath('//*[@class="note-author"]/text()').extract()[0].encode('utf8')
            doubannote_item['pub_date'] = \
                sel.xpath('//*[@class="pub-date"]/text()').extract()[0].encode('utf8')
            contents = sel.xpath('//*[@id="link-report"]//text()').extract()
            for content in contents:
                if content.strip():
                    # 50 bytes most for not snippet
                    doubannote_item['snippet'] = content[:100].encode('utf8')
                    break
            doubannote_item['comment_num'] = len(sel.xpath('//*[@class="comment-item"]').extract())
            tags = ''
            for tag in sel.xpath('//*[@class="mod-tags"]/a/text()').extract():
                #  self.log('tag:%s' % tag)
                tags = tags + ' | ' + tag.encode('utf8')
            doubannote_item['tags'] = tags
            yield doubannote_item

#  '''
        # more peoples
        peoples = sel.xpath('//*[@class="note-author"]/@href').extract()
        for people in peoples:
            people_note = people + 'notes'
            self.log('response url: %s new people: %s' % (response.url, people_note))
            yield scrapy.Request(url=people_note, callback=self.parse)
        # more peoples in comments
        peoples = sel.xpath('//*[@class="author"]/a/@href').extract()
        for people in peoples:
            people_note = people + 'notes'
            self.log('response url: %s new comment people: %s' % (response.url, people_note))
            yield scrapy.Request(url=people_note, callback=self.parse)

        # more note-list by paginator
        if response.url.startswith('https://www.douban.com/people'):
            note_lists = sel.xpath('//*[@class="paginator"]/a/@href').extract()
            for note in note_lists:
                self.log('response url: %s new note_list: %s' % (response.url, note))
                yield scrapy.Request(url=note, callback=self.parse)

        # more channels
        # todo: channel 需要js渲染
        #  channels = sel.xpath('//a/@href').re(u'https://www.douban.com/channel/\d+')
        #  for channel in channels:
            #  self.log('response url: %s new channel: %s' % (response.url, channel))
            #  yield scrapy.Request(url=channel, callback=self.parse)

        # all notes-url on this pages
        new_notes = sel.xpath('//a/@href').re(u'https://www.douban.com/note/\d+/')
        for note in new_notes:
            self.log('response url: %s new note: %s' % (response.url, note))
            yield scrapy.Request(url=note, callback=self.parse)
#  '''
