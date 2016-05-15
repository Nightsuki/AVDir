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


class LogoutHandler(BaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.clear_cookie("_user")
        self.redirect("/admin/login")


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
        archive_list = Archive.select().order_by(Archive.id.desc())
        self.render("archive_list.html", archive_list=archive_list)


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
        archive_id = args
        archive = Archive.select().where(Archive.id == archive_id).first()
        if archive:
            self.render("archive_edit.html", archive=archive)


class UserListHandler(AdminBaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    @check_role(["User", "Admin"])
    def get(self, *args, **kwargs):
        user_list = User.select().order_by(User.id.desc())
        self.render("user_list.html", user_list=user_list)


class UserAddHandler(AdminBaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    @check_role(["User", "Admin"])
    def get(self, *args, **kwargs):
        self.render("user_add.html")


class UserEditHandler(AdminBaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    @check_role(["User", "Admin"])
    def get(self, *args, **kwargs):
        self.render("user_edit.html")




