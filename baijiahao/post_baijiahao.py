#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib2
import json
import markdown2
import httplib
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# article
ORIGIN_MARKDOWN = '2018-12-30-xcz-reading.markdown'
COVER_IMAGE = 'https://izualzhy.cn/assets/images/xincanzhe.png'

#  API
HOST = 'https://izualzhy.cn/'
PUBLISH_API = 'http://baijiahao.baidu.com/builderinner/open/resource/article/publish'
#  配置APP_ID APP_TOKEN，从开发者页面(https://baijiahao.baidu.com/builder/rc/develop)获取
APP_ID = '1598771538853672'
APP_TOKEN = 'e42b80660f35109f3632c33aec15c670'


#  从原始markdown文件获取title
def generate_title():
    with open(ORIGIN_MARKDOWN, 'r') as f:
        contents = f.readlines()
        #  获取具体title，例如contents[2]=title: "leveldb笔记之11:LRUCache的实现"
        return contents[2][8:-1]


#  根据原始markdown文件生成对应的富文本
def generate_contents(original_url):
    HTML_HEADER = '''
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en-us">
        <head>
            <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        </head>
        <body>
    '''
    HTML_TAILOR = '''
        </body>
    </html>
    '''
    html = markdown2.markdown_path(ORIGIN_MARKDOWN, extras=['fenced-code-blocks'])
    html = html.replace('/assets/images', HOST + 'assets/images')

    ORIGINAL_WARNING = '由于百家号对代码排版较差，而且在富文本中丢格式，可以直接查看网站原文:' + original_url
    content = HTML_HEADER + ORIGINAL_WARNING + html + HTML_TAILOR
    with open('post_baijiahao.html', 'w') as f:
        f.write(content)
    return content


#  组装数据
def pack_publish_data():
    publish_data = {}
    publish_data['app_id'] = APP_ID
    publish_data['app_token'] = APP_TOKEN

    #  从文件名获取url对应的path
    url_path = re.search("[0-9]+-[0-9]+-[0-9]+-(.*).markdown", ORIGIN_MARKDOWN).group(1)
    content_url = HOST + url_path

    #  直接curl获取是最方便的，不过测试几次都显示推送成功，但是百家号平台实际没有看到
    #  content = urllib2.urlopen(content_url).read()
    publish_data['title'] = generate_title()
    publish_data['content'] = generate_contents(content_url)
    publish_data['origin_url'] = content_url
    cover_images = [
        {'src': COVER_IMAGE},
    ]
    publish_data['cover_images'] = json.dumps(cover_images).replace('/', '\/')
    #  publish_data['cover_images'] = json.dumps(cover_images)
    publish_data['is_original'] = 1

    return json.dumps(publish_data)


#  组装数据post 百家号API接口
def post_article():
    httplib.HTTPConnection.debuglevel = 1

    post_data = pack_publish_data()
    print len(post_data)
    request = urllib2.Request(PUBLISH_API, data=post_data)
    opener = urllib2.build_opener(urllib2.HTTPHandler(httplib.HTTPConnection.debuglevel | 1))
    print opener.open(request).read()

if __name__ == '__main__':
    post_article()
