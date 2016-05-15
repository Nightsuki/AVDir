# coding=utf-8
import tornado.web
from controller.base import BaseHandler, NotFoundHandler
from tornado import gen
from database import *
from itertools import groupby
from util.function import humantime


class ArchiveHandler(BaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        slug = args[0]
        try:
            archive = Archive.get((Archive.slug == slug) & (Archive.type == 0))
            self.render("archive.html", archive=archive)
        except:
            self.redirect("/diracsea")


class PageHandler(BaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        slug = args[0]
        try:
            archive = Archive.get((Archive.slug == slug) & (Archive.type == 1))
            self.render("page.html", archive=archive)
        except:
            self.redirect("/diracsea")


class ArchiveLineHandler(BaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        archives = Archive.select().where((Archive.status == 1) & (Archive.type == 0)).order_by(
            Archive.published_time.desc())
        archives_groups = [{'year': year, 'archives': list(archives)}
                           for year, archives in groupby(archives, key=lambda a: humantime(a.published_time, "%Y"))]
        self.render("timeline.html", archives_groups=archives_groups, first_title="Archives")
