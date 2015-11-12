# coding=utf-8
import tornado.web
from tornado import gen
from controller.base import BaseHandler
from util.function import ajax_need_login
from database import *


class AjaxHandler(BaseHandler):
    def prepare(self):
        super(AjaxHandler, self).prepare()

    def post(self, *args, **kwargs):
        action = "_%s_action" % args[0]
        if hasattr(self, action):
            getattr(self, action)()
        else:
            self._json(0, "No way here!")

    def _json(self, code, result=""):
        if type(result) == str:
            result = result.decode("utf8")
        data = {
            "code": code,
            "result": result
        }
        self.write(data)
        raise tornado.web.Finish()

    @tornado.web.asynchronous
    @gen.coroutine
    def _login_action(self):
        username = self.get_body_argument("username", default=None)
        password = self.get_body_argument("password", default=None)
        if username and password:
            user = User.select().where(User.username == username).first()
            if user and user.check_password(password):
                self.set_user(user)
                self._json("success")
            else:
                self._json("fail", "账号或密码错误")
        self._json("fail", "请填写账号和密码")
