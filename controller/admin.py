# coding=utf-8
import os
import tornado.web
from controller.base import BaseHandler
from tornado import gen
from util.function import check_role
from database import User, Archive


class AdminBaseHandler(BaseHandler):
    def get_template_path(self):
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), "../theme/admin/templates")


class LoginHandler(AdminBaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.render("login.html")


class IndexHandler(AdminBaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    @check_role(["User", "Admin"])
    def get(self, *args, **kwargs):
        self.render("index.html")
        

class ArchiveListHandler(AdminBaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    @check_role(["User", "Admin"])
    def get(self, *args, **kwargs):
        self.render("archive_list.html")


class ArchiveAddHandler(AdminBaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    @check_role(["User", "Admin"])
    def get(self, *args, **kwargs):
        self.render("archive_add.html")


class ArchiveEditHandler(AdminBaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    @check_role(["User", "Admin"])
    def get(self, *args, **kwargs):
        self.render("archive_edit.html")




