# coding=utf-8
from peewee import *
from playhouse.shortcuts import RetryOperationalError
from werkzeug.security import generate_password_hash, check_password_hash
import time
import sys
import yaml
import os
import json


if os.environ.get("AVDIR_ENV") == 'prod':
    config_env = "prod"
else:
    config_env = "dev"

config_filename = "config.yaml"
config = {}

try:
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), config_filename), "r") as fin:
        config = yaml.load(fin)
except:
    print("cannot found config.yaml file")
    sys.exit(0)


class RetryDB(RetryOperationalError, MySQLDatabase):
    pass


try:
    db = RetryDB(config["database"][config_env]["dbname"],
                 user=config["database"][config_env]["user"],
                 host=config["database"][config_env]["host"],
                 port=config["database"][config_env]["port"],
                 password=config["database"][config_env]["password"],
                 autocommit=True, autorollback=True)
except:
    print("cannot connect Mysql, check the config.yaml")
    sys.exit(0)

print("Connected to DB.")


class BaseModel(Model):
    id = PrimaryKeyField(null=False)
    created_time = IntegerField(null=False, default=0)

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)
        self.created_time = int(time.time())

    class Meta:
        database = db
        auto_increment = True


class Config(BaseModel):
    class Meta:
        db_table = 'configs'

    key = CharField(null=False, default="")
    value = CharField(null=False, default="")

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Config({key!r})>'.format(key=self.key)


class User(BaseModel):
    class Meta:
        db_table = 'users'

    username = CharField(unique=True, null=False, default="")
    nickname = CharField(null=False, default="默认用户")
    email = CharField(unique=True, null=False, default="")
    avatar = CharField(default="", null=False)
    password = CharField(null=False, default="")
    role = IntegerField(null=False, default=0)
    last_time = IntegerField(null=False, default=0)
    last_ip = CharField(null=False, default="")

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)

    @property
    def role(self):
        if self.role == 0:
            return "User"
        if self.role == 1:
            return "Admin"

    def set_password(self, password):
        self.password = generate_password_hash(password, method="pbkdf2:sha256")

    def set_last(self, ip):
        self.last_ip = ip
        self.last_time = int(time.time())

    def check_password(self, value):
        return check_password_hash(self.password, value)

    def __repr__(self):
        return '<User({username!r})>'.format(username=self.username)


class Archive2Tag(BaseModel):
    class Meta:
        db_table = 'archives_tags'

    archive_id = IntegerField(default=0, null=False)
    tag_id = IntegerField(default=0, null=False)

    def __init__(self, *args, **kwargs):
        super(Archive2Tag, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Archive2Tag({id!r})>'.format(title=self.id)


class Tag(BaseModel):
    class Meta:
        db_table = 'tags'

    content = CharField(null=False, default="")

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Tag({content!r})>'.format(title=self.content)


class Archive(BaseModel):
    class Meta:
        db_table = 'archives'

    title = CharField(null=False, default="")
    slug = CharField(null=False, default="")
    content = TextField(null=False, default="")
    type = CharField(null=False, default="")
    user = ForeignKeyField(User)
    status = IntegerField(null=False, default=0)  # 0未发布 1已发布
    modified_time = IntegerField(null=False, default=0)
    published_time = IntegerField(null=False, default=0)

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)

    def get_tags(self):
        query = Archive2Tag.select(Archive2Tag.tag_id).where(Archive2Tag.archive_id == self.id)
        tag_ids = [one.tag_id for one in query]
        tag_query = Tag.select(Tag.content).where(Tag.id << tag_ids)
        return [one.content for one in tag_query]

    def __repr__(self):
        return '<Archive({title!r})>'.format(title=self.title)


db.create_tables([Config, User, Archive, Tag, Archive2Tag], safe=True)
