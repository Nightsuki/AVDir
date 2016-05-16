# coding=utf-8
import tornado.web
from tornado import gen
from controller.base import BaseHandler
from util.function import ajax_check_role
from database import *


class AjaxHandler(BaseHandler):
    def prepare(self):
        super(AjaxHandler, self).prepare()

    def post(self, *args, **kwargs):
        action = "_%s_action" % args[0]
        if hasattr(self, action):
            getattr(self, action)()
        else:
            self._json("fail", "404")

    def _json(self, status, result=""):
        data = {
            "status": status,
            "result": result
        }
        self.write(data)
        raise tornado.web.Finish()

    @tornado.web.asynchronous
    @gen.coroutine
    def _login_action(self):
        username = self.get_json_argument("username", default="", strip=True)
        password = self.get_json_argument("password", default="", strip=True)
        if username and password:
            user = User.select().where(User.username == username.lower()).first()
            if user and user.check_password(password):
                user.set_last(self.get_ip())
                self.set_user(user)
                self._json("success", "登录成功")
            else:
                self._json("fail", "账号或密码错误")
        self._json("fail", "请填写账号和密码")

    @tornado.web.asynchronous
    @gen.coroutine
    @ajax_check_role(["User", "Admin"])
    def _archive_action(self):
        action = self.get_json_argument("action", default=None)
        archive_id = self.get_json_argument("archive_id", default=None)
        title = self.get_json_argument("title", default="")
        content = self.get_json_argument("content", default="")
        slug = self.get_json_argument("slug", default="")
        type = self.get_json_argument("type", default=0)
        tags = self.get_json_argument("tags", default=[])
        if action == "add":
            if title and content and slug and type:
                archive_query = Archive()
                archive_query.user_id = self.current_user["id"]
                archive_query.title = title
                archive_query.content = content
                archive_query.slug = slug
                archive_query.type = type
                archive_query.modified_time = int(time.time())
                archive_query.published_time = int(time.time())
                archive_query.status = 1
                archive_query.save()
                archive_query.tag = tags
                self._json("success", "发表成功")
            self._json("fail", "请填写完整")
        if action == "edit":
            archive_query = Archive.select().where(Archive.id == archive_id).first()
            if archive_id and archive_query and title and content and slug and type:
                if self.current_user["id"] == archive_query.user.id or self.current_user["role"] == "Admin":
                    archive_query.title = title
                    archive_query.content = content
                    archive_query.tag = tags
                    archive_query.slug = slug
                    archive_query.type = type
                    archive_query.status = 1
                    archive_query.save()
                    self._json("success", "修改成功")
                self._json("fail", "无权操作")
            self._json("fail", "请填写完整")
        if action == "del":
            archive_query = Archive.select().where(Archive.id == archive_id).first()
            if archive_id and archive_query:
                if self.current_user["id"] == archive_query.author.id or self.current_user["role"] == "Admin":
                    del archive_query.tag
                    archive_query.delete_instance()
                    self._json("success", "删除成功")
                self._json("success", "无权操作")
            self._json("success", "不存在的文章")
        self._json("fail", "错误的姿势")

    @tornado.web.asynchronous
    @gen.coroutine
    @ajax_check_role(["User", "Admin"])
    def _user_action(self):
        action = self.get_json_argument("action", default=None)
        user_id = self.get_json_argument("user_id", default=None)
        username = self.get_json_argument("username", default="")
        nickname = self.get_json_argument("nickname", default="默认用户")
        password = self.get_json_argument("password", default="")
        email = self.get_json_argument("email", default="")
        role = self.get_json_argument("role", default=0)
        if action == "add":
            if self.current_user["role"] == "Admin" and (username and nickname and password and email):
                user_query = User()
                user_query.username = username
                user_query.nickname = nickname
                user_query.set_password(password)
                user_query.email = email
                user_query.role = role
                user_query.save()
                self._json("success", "创建成功")
        if action == "edit":
            user_query = User.select().where(User.id == user_id).first()
            if user_id and user_query:
                if self.current_user["id"] == user_query.id or self.current_user["role"] == "Admin":
                    if nickname: user_query.nickname = nickname
                    if password: user_query.set_password(password)
                    if email: user_query.email = email
                    if role and self.current_user["role"] == "Admin": user_query.role = role
                    user_query.save()
                    self._json("success", "修改成功")
        if action == "del":
            user_query = User.select().where(User.id == user_id).first()
            if user_id and user_query:
                if self.current_user["role"] == "Admin":
                    user_query.delete_instance()
                    self._json("success", "删除成功")
        self._json("fail", "姿势错误")
