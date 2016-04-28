# coding=utf-8
import tornado.web
from util.function import humantime, json, time_span, markdown


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.site = self.settings.get("site")
        self.is_pjax = False

    def prepare(self):
        self.set_header("X-XSS-Protection", "1; mode=block")
        self.set_header("X-UA-Compatible", "IE=edge,chrome=1")
        self.set_header("X-Powered-by", "AVDir")
        self.is_pjax = True if self.request.headers.get('X-Pjax', None) else False

    def set_user(self, user):
        if not user:
            return None
        try:
            user = {
                "id": user.id,
                "role": user.get_role(),
                "username": user.username,
                "nickname": user.nickname
            }
            user = json.dumps(user)
            self.set_secure_cookie("_user", user, httponly=True, secure=True)
        except:
            return None

    @staticmethod
    def _get_json_argument(name, default, source, strip=False):
        try:
            body_json = json.loads(source.decode('utf-8'))
        except Exception as e:
            print(e)
            return None
        value = body_json[name] if name in body_json else default
        if strip and value:
            value = value.strip()
        return value

    def get_json_argument(self, name, default=None, strip=False):
        return self._get_json_argument(name, default, self.request.body, strip)

    def get_current_user(self):
        try:
            user = self.get_secure_cookie("_user")
            assert user
        except:
            user = None
        return user

    @staticmethod
    def static_admin_url(path):
        return "/admin/static/{}".format(path)

    def render(self, template_name, **kwargs):
        kwargs["humantime"] = humantime
        kwargs["time_span"] = time_span
        kwargs["markdown"] = markdown
        kwargs["static_admin_url"] = self.static_admin_url
        for one in self.site:
            if one not in kwargs:
                kwargs[one] = self.site[one]
        return super(BaseHandler, self).render(template_name, **kwargs)

    def redirect(self, url, permanent=False, status=None):
        super(BaseHandler, self).redirect(url, permanent, status)
        raise tornado.web.Finish()

    def get_ip(self):
        if self.request.headers.get('X-Forwarded-For'):
            return self.request.headers.get('X-Forwarded-For')
        else:
            return self.request.remote_ip


class NotFoundHandler(BaseHandler):
    def prepare(self):
        BaseHandler.prepare(self)

    def get(self, *args, **kwargs):
        self.set_status(404)
        self.render("404.html")

    def post(self, *args, **kwargs):
        self.get(*args, **kwargs)
