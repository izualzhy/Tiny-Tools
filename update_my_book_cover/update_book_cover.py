#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: update_book_cover.py
Author: izualzhy(izualzhy@163.com)
Date: 2017/12/24 17:14:29
"""

import urllib2
import bs4
import collections


##
# @brief update book cover href in http://izualzhy.cn/books.html
class BookCoverUpdater:
    def __init__(self):
        self.__book_info_flag = '- '
        self.__book_item_sep = ': '

    def update(self):
        with open('new_books.yml', 'w') as new_books_file:
            for book_info in self.__read_orignal_book_info():
                self.__update_cover_url(book_info)
                start_key = self.__book_info_flag
                for item in book_info:
                    new_books_file.write(start_key)
                    new_books_file.write(item + self.__book_item_sep + book_info[item] + '\n')
                    start_key = ' ' * len(self.__book_info_flag)
                new_books_file.write('\n')

    def __read_orignal_book_info(self):
        book_info = collections.OrderedDict()
        with open('books.yml', 'r') as books_file:
            for line in books_file:
                line = line.strip()
                if line.startswith(self.__book_info_flag):
                    yield book_info
                    book_info = collections.OrderedDict()
                    # skip __book_info_flag
                    line = line[2:]
                key_values = line.split(self.__book_item_sep)
                if len(key_values) == 2:
                    book_info[key_values[0]] = key_values[1]
            yield book_info

    def __update_cover_url(self, book_info):
        if 'douban_link' in book_info:
            try:
                soup = bs4.BeautifulSoup(urllib2.urlopen(book_info['douban_link']).read(), 'lxml')
                book_info['cover'] = soup.find_all('a', class_='nbg')[0].attrs['href']
            except urllib2.HTTPError:
                print "%s return HTTPError" % (book_info['douban_link'])
            except IndexError:
                print "%s return IndexError" % (book_info['douban_link'])

if __name__ == '__main__':
    book_cover_updater = BookCoverUpdater()
    book_cover_updater.update()
