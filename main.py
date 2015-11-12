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
    "session": {
        "switch": True,
        "driver": "redis",
        "driver_settings": {
            "host": "localhost",
            "port": 6379,
            "db": 1
        },
        "force_persistence": False,
        "cache_driver": True,
        "cookie_config": {
            "expires_days": 1,
            "domain": ".ymr.me",
            "httponly": True
        },
    },
    "cache": {
        "switch": True,
        "driver": "redis",
        "driver_settings": {
            "host": "localhost",
            "port": 6379,
            "db": 10
        }
    },
    "thread_pool": futures.ThreadPoolExecutor(4)
}

if os.environ.get("KOUSHAO_ENV") == 'prod':
    config_env = "prod"
else:
    config_env = "dev"
print(config_env)

config = {}
try:
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), setting["config_filename"]), "r") as fin:
        config = yaml.load(fin)
    setting["site"] = config["site"]
    setting["static_path"] = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                          "theme/%s/static" % config["site"]["theme"])
    setting["template_path"] = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                            "theme/%s/templates" % config["site"]["theme"])
    if setting["session"]["switch"] and "session" in config:
        setting["session"]["driver_settings"] = config["session"][config_env]
        session = redis.Redis(**setting["cache"]["driver_settings"])
        setting["session"] = session
    if setting["cache"]["switch"] and "cache" in config:
        setting["cache"]["driver_settings"] = config["cache"][config_env]
        cache = redis.Redis(**setting["cache"]["driver_settings"])
        setting["cache"] = cache
except Exception, e:
    print(e)
    print "cannot found config.yaml file"
    sys.exit(0)

application = tornado.web.Application([
    (r"^/", "controller.main.MainHandler"),
    (r"^/archives", "controller.archive.ArchiveLineHandler"),
    (r"^/ajax/([a-z]+)", "controller.ajax.AjaxHandler"),
    (r"^/archive/(.*)", "controller.archive.ArchiveHandler"),
    (r"^/page/([\d]+)?", "controller.main.PageHandler"),
    (r"^/tag/(.*)", "controller.main.TagHandler"),
    (r"^/feed", "controller.main.FeedHandler"),
    (r"^/diracsea", "controller.base.NotFoundHandler"),
    (r"^/(.*)", "controller.archive.PageHandler"),
], **setting)

if __name__ == "__main__":
    try:
        application.listen(tornado.options.options.port)
        tornado.ioloop.IOLoop.instance().start()
    except:
        import traceback

        print traceback.print_exc()
    finally:
        sys.exit(0)
