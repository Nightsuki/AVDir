# coding=utf-8
import os
import json
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
        archive_list = Archive.select().where(Archive.user_id == self.current_user["id"]).order_by(Archive.id.desc())
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


class UploadHandler(AdminBaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    @check_role(["User", "Admin"])
    def post(self, *args, **kwargs):
        result = {"success": 0, "message": "上传失败"}
        if self.request.files:
            content = self.request.files["editormd-image-file"][0]["body"]
            filename = self.request.files["editormd-image-file"][0]["filename"]
            url = self.upload(content, filename)
            if url:
                result = {"success": 1,
                          "message": "上传成功",
                          "url": url}
        return self.write(json.dumps(result))


class UserListHandler(AdminBaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    @check_role(["Admin"])
    def get(self, *args, **kwargs):
        user_list = User.select().order_by(User.id.desc())
        self.render("user_list.html", user_list=user_list)


class UserAddHandler(AdminBaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    @check_role(["Admin"])
    def get(self, *args, **kwargs):
        self.render("user_add.html")


class UserEditHandler(AdminBaseHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    @check_role(["Admin"])
    def get(self, *args, **kwargs):
        user = User.select().where(User.id == args).first()
        if user:
            self.render("user_edit.html", user=user)
