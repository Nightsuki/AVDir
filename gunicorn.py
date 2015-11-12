# -*- coding:utf-8 -*-
# !/usr/bin/env python

# coding: utf-8

import gevent.monkey
import multiprocessing


gevent.monkey.patch_all()

bind = 'unix:/var/run/avdir.sock'
# bind = "0.0.0.0:8001"
max_requests = 10000
keepalive = 5

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'tornado'

loglevel = 'error'
errorlog = '-'

x_forwarded_for_header = 'X-FORWARDED-FOR'

secure_scheme_headers = {
    'X-SCHEME': 'https',
}
