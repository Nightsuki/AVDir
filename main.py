#!/usr/bin/python
import tornado.ioloop
import tornado.web
import tornado.options
import sys
import os
import yaml
from concurrent import futures
import controller.base
import redis

tornado.options.define("port", default=5555, help="Run server on a specific port", type=int)
tornado.options.parse_command_line()

setting = {
    "cookie_secret": "17a18595b03aef1def118e8ed4e5b00d",
    "config_filename": "config.yaml",
    "compress_response": True,
    "default_handler_class": controller.base.NotFoundHandler,
    "xsrf_cookies": False,
    "autoreload": True,
    "thread_pool": futures.ThreadPoolExecutor(4)
}

if os.environ.get("AVDIR_ENV") == 'prod':
    config_env = "prod"
else:
    config_env = "dev"
    setting["serve_traceback"] = True
print(config_env)

config = {}
try:
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), setting["config_filename"]), "r", encoding="utf-8") as fin:
        config = yaml.load(fin)
    theme = config["site"]["theme"]
    setting["site"] = config["site"]
    setting["qiniu"] = config["qiniu"]
    setting["static_path"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "theme/{}/static".format(theme))
    setting["static_admin_path"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "theme/admin/static")
    setting["template_path"] = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                            "theme/{}/templates".format(theme))
except Exception as e:
    print(e)
    print("cannot found config.yaml file")
    sys.exit(0)

application = tornado.web.Application([
    (r"^/", "controller.main.MainHandler"),

    (r"^/ajax/([a-z]+)", "controller.ajax.AjaxHandler"),

    (r"^/archives", "controller.archive.ArchiveLineHandler"),
    (r"^/archive/(.*)", "controller.archive.ArchiveHandler"),

    (r"^/page/([\d]+)?", "controller.main.PageHandler"),
    (r"^/tag/(.*)", "controller.main.TagHandler"),
    (r"^/feed", "controller.main.FeedHandler"),

    (r"^/admin", "controller.admin.IndexHandler"),
    (r"^/admin/login", "controller.admin.LoginHandler"),
    (r"^/admin/logout", "controller.admin.LogoutHandler"),
    (r"^/admin/archive/add", "controller.admin.ArchiveAddHandler"),
    (r"^/admin/archive/edit/([0-9]+)", "controller.admin.ArchiveEditHandler"),
    (r"^/admin/archive/list", "controller.admin.ArchiveListHandler"),
    (r"^/admin/user/add", "controller.admin.UserAddHandler"),
    (r"^/admin/user/edit/([0-9]+)", "controller.admin.UserEditHandler"),
    (r"^/admin/user/list", "controller.admin.UserListHandler"),

    (r"/admin/static/(.*)", tornado.web.StaticFileHandler, dict(path=setting["static_admin_path"])),
    (r"^/diracsea", "controller.base.NotFoundHandler"),
    (r"^/(.*)", "controller.archive.PageHandler"),
], **setting)

if __name__ == "__main__":
    try:
        application.listen(tornado.options.options.port)
        tornado.ioloop.IOLoop.instance().start()
    except:
        import traceback
        print(traceback.print_exc())
    finally:
        sys.exit(0)
