#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import datetime

from doubannote.settings import PROXY_LIST_FILE


class ProxyMiddleware(object):
    def __init__(self):
        # long long ago
        self._last_reload_time = datetime.datetime(1922, 2, 2, 2, 2, 2, 2)
        self._proxies = []

    def _check_if_need_reload_proxies(self):
        #  print '_check_if_need_reload_proxies'
        current = datetime.datetime.now()
        # reload interval is 10800 seconds
        # which is got from 66ip
        # http://www.66ip.cn/nmtq.php?getnum=800&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=
        #  if (current - self._last_reload_time).seconds >= 10:
        if (current - self._last_reload_time).seconds >= 10800:
            self._proxies = []
            with open(PROXY_LIST_FILE, 'r') as f:
                for proxy in f:
                    self._proxies.append(proxy.strip())
            self._last_reload_time = datetime.datetime.now()
            print 'proxy reloaded.'
        else:
            pass
            #  print 'no need to reload proxy.'

    def process_request(self, request, spider):
        try:
            # 30 percent
            if (random.randint(1, 10) <= 3):
                return

            self._check_if_need_reload_proxies()
            proxy = random.choice(self._proxies)
            if proxy:
                #  print 'proxy choosed:', proxy
                request.meta['proxy'] = 'http://' + proxy
        except:
            print 'maybe reload proxy failed bcz mutex? forgot it.'
