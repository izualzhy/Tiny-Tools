#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from doubannote.settings import USER_AGENTS


class UserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = random.choice(USER_AGENTS)
        if ua:
            request.headers.setdefault('User-Agent', ua)
