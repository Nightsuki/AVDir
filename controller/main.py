# coding=utf-8
import tornado.web
from controller.base import BaseHandler
from tornado import gen
from database import Tag, Archive2Tag, Archive
from util.function import humantime
from itertools import groupby


class MainHandler(BaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        count = Archive.select().count()
        maxpage = count / 6 + 1
        archives = Archive.select().where((Archive.status == 1) & (Archive.type == 0)).order_by(
            Archive.created_time.desc()).offset(0).limit(6)
        self.render("list.html", archives=archives, maxpage=maxpage, page=1)


class PageHandler(BaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        page = int(args[0]) if int(args[0]) else 1
        offset = (page - 1) * 6
        count = Archive.select().count()
        maxpage = count / 6 + 1
        archives = Archive.select().where((Archive.status == 1) & (Archive.type == 0)).order_by(
            Archive.created_time.desc()).offset(offset).limit(6)
        self.render("list.html", archives=archives, maxpage=maxpage, page=page)


class TagHandler(BaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        tag = args[0]
        tag_query = Tag.select().where(Tag.content == tag).first()
        if tag_query:
            archives2tag_query = Archive2Tag.select(Archive2Tag.archive_id).where(Archive2Tag.tag_id == tag_query.id)
            archive_ids = [one.archive_id for one in archives2tag_query]
            archives = Archive.select().where(
                (Archive.id << archive_ids) & (Archive.status == 1) & (Archive.type == 0)).order_by(
                Archive.published_time.desc())
            archives_groups = [{'year': year, 'archives': list(archives)}
                               for year, archives in groupby(archives, key=lambda a: humantime(a.published_time, "%Y"))]
            self.render("timeline.html", archives_groups=archives_groups, first_title="Tag: %s" % tag)


class FeedHandler(BaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        archives = Archive.select().where((Archive.status == 1) & (Archive.type == 0)).order_by(
            Archive.published_time.desc())
        self.set_header("Content-Type", "application/xml")
        self.render("feed.xml", archives=archives)
