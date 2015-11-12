#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os, string, random, hashlib, time, re, datetime
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
import json
import mistune


@gen.coroutine
def shorturl(url):
    url = "http://api.t.sina.com.cn/short_url/shorten.json?source=3271760578&url_long=%s" % url
    response = yield gen.Task(
        AsyncHTTPClient().fetch, url, method="GET")
    result = json.loads(response.body)
    short_url = result["url_short"]
    raise gen.Return(short_url)


def md5(str):
    '''
    计算简单的md5 hex格式字符串

    :param str: 原字符串
    :return: 返回的32尾hex字符串
    '''
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


def markdown(text):
    markdown = mistune.Markdown(escape=True, hard_wrap=True)
    return markdown(text)


def ajax_need_login(func):
    '''
    修饰器，修饰prepare方法，需要登录才可使用。

    :param func: prepare方法
    :return: 处理过的prepare方法
    '''

    def do_prepare(self, *args, **kwargs):
        user = self.get_current_user()
        if not user:
            self._json(-1, "请登录后使用")
        return func(self, *args, **kwargs)
    return do_prepare


def need_login(func):
    '''
    修饰器，修饰prepare方法，需要登录才可使用。

    :param func: prepare方法
    :return: 处理过的prepare方法
    '''

    def do_prepare(self, *args, **kwargs):
        user = self.get_current_user()
        if not user:
            self.write('''<script language="javascript">alert("请登录后使用");window.history.back(-1);</script>''')
            return self.finish()
        return func(self, *args, **kwargs)
    return do_prepare


def intval(str):
    '''
    将字符串强制转换成数字

    :param str: 输入的字符串
    :return: 数字
    '''
    if type(str) is int: return str
    try:
        ret = re.match(r"^(\-?\d+)[^\d]?.*$", str).group(1)
        ret = int(ret)
    except:
        ret = 0
    return ret


def humansize(file):
    '''
    计算文件大小并输出为可读的格式（如 1.3MB）

    :param file: 文件路径
    :return: 可读的文件大小
    '''
    if os.path.exists(file):
        nbytes = os.path.getsize(file)
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        if nbytes == 0: return '0 B'
        i = 0
        while nbytes >= 1024 and i < len(suffixes) - 1:
            nbytes /= 1024.
            i += 1
        f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, suffixes[i])
    else:
        return u"未知"


def humantime(t=None, format="%Y年%m月%d日 %H:%M", span=False):
    '''

    %y 两位数的年份表示（00-99）
    %Y 四位数的年份表示（000-9999）
    %m 月份（01-12）
    %d 月内中的一天（0-31）
    %H 24小时制小时数（0-23）
    %I 12小时制小时数（01-12）
    %M 分钟数（00=59）
    %S 秒（00-59）

    %a 本地简化星期名称
    %A 本地完整星期名称
    %b 本地简化的月份名称
    %B 本地完整的月份名称
    %c 本地相应的日期表示和时间表示
    %j 年内的一天（001-366）
    %p 本地A.M.或P.M.的等价符
    %U 一年中的星期数（00-53）星期天为星期的开始
    %w 星期（0-6），星期天为星期的开始
    %W 一年中的星期数（00-53）星期一为星期的开始
    %x 本地相应的日期表示
    %X 本地相应的时间表示
    %Z 当前时区的名称
    %% %号本身

    :param t: 时间戳，默认为当前时间
    :param format: 格式化字符串
    :return: 当前时间字符串
    '''
    if not t:
        t = time.time()
    if span:
        return time_span(t)
    return time.strftime(format, time.localtime(t))


def time_span(ts):
    '''
    计算传入的时间戳与现在相隔的时间

    :param ts: 传入时间戳
    :return: 人性化时间差
    '''
    delta = datetime.datetime.now() - datetime.datetime.fromtimestamp(ts)
    if delta.days >= 365:
        return '%d年前' % int(delta.days / 365)
    elif delta.days >= 30:
        return '%d个月前' % int(delta.days / 30)
    elif delta.days > 0:
        return '%d天前' % delta.days
    elif delta.seconds < 60:
        return "%d秒前" % delta.seconds
    elif delta.seconds < 60 * 60:
        return "%d分钟前" % int(delta.seconds / 60)
    else:
        return "%d小时前" % int(delta.seconds / 60 / 60)


def random_str(randomlength=12):
    '''
    获得随机字符串，包含所有大小写字母+数字

    :param randomlength: 字符串长度，默认12
    :return: 随机字符串
    '''
    a = list(string.ascii_letters + string.digits)
    random.shuffle(a)
    return ''.join(a[:randomlength])


