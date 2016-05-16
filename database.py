# coding=utf-8
from peewee import *
from playhouse.shortcuts import RetryOperationalError
from werkzeug.security import generate_password_hash, check_password_hash
import time
import sys
import yaml
import os
from controller.tag import TagHandle


if os.environ.get("AVDIR_ENV") == 'prod':
    config_env = "prod"
else:
    config_env = "dev"

config_filename = "config.yaml"
config = {}

try:
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), config_filename), "r", encoding="utf-8") as fin:
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
        super(Config, self).__init__(*args, **kwargs)

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
        super(User, self).__init__(*args, **kwargs)

    @property
    def get_role(self):
        if self.role == 0:
            return "User"
        if self.role == 1:
            return "Admin"

    def set_password(self, password):
        self.password = generate_password_hash(password, method="pbkdf2:sha256")

    def set_last(self, ip):
        self.last_ip = ip
        self.last_time = int(time.time())
        self.save()

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
        return '<Archive2Tag({}!r})>'.format(self.id)


class Tag(BaseModel):
    class Meta:
        db_table = 'tags'

    content = CharField(null=False, default="")

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Tag({}!r})>'.format(self.content)


class Archive(BaseModel):
    class Meta:
        db_table = 'archives'

    title = CharField(null=False, default="")
    slug = CharField(null=False, default="")
    content = TextField(null=False, default="")
    type = IntegerField(null=False, default=0)  # 0文章  1单页
    user_id = IntegerField(null=False, default=0)
    status = IntegerField(null=False, default=0)  # 0未发布 1已发布
    modified_time = IntegerField(null=False, default=0)
    published_time = IntegerField(null=False, default=0)

    def __init__(self, *args, **kwargs):
        super(Archive, self).__init__(*args, **kwargs)

    @property
    def recommend_archive(self):
        tag_ids = self.tag_ids
        result = []
        if len(tag_ids) > 0:
            query = Archive2Tag.select().where((Archive2Tag.tag_id << tag_ids) & (Archive2Tag.archive_id != self.id))
            archive_ids = [one.archive_id for one in query]
            if len(archive_ids) > 0:
                result = Archive.select(Archive.title, Archive.slug).where(Archive.id << archive_ids)
        return result

    @staticmethod
    def tag_exist(name):
        query = Tag.select().where(Tag.content == name).first()
        return query if query else False

    def insert_tag(self, name):
        query = self.tag_exist(name)
        if not query:
            query = Tag()
            query.content = name
            query.save()
        return query

    @property
    def tag_text(self):
        tag_list = self.tag
        result = ""
        if len(tag_list) > 0:
            result = tag_list[0]
        for i in range(1, len(tag_list)):
            result += ",{}".format(tag_list[i])
        return result

    @property
    def tag_ids(self):
        query = Archive2Tag.select(Archive2Tag.tag_id).where(Archive2Tag.archive_id == self.id)
        tag_ids = [one.tag_id for one in query]
        return tag_ids

    @property
    def tag(self):
        query = Archive2Tag.select(Archive2Tag.tag_id).where(Archive2Tag.archive_id == self.id)
        tag_ids = [one.tag_id for one in query]
        tag_query = Tag.select(Tag.content).where(Tag.id << tag_ids) if len(tag_ids) > 0 else []
        return [one.content for one in tag_query]

    @tag.setter
    def tag(self, tag_list):
        archive2tag_query = Archive2Tag.delete().where(Archive2Tag.archive_id == self.id)
        archive2tag_query.execute()
        new_insert = []
        for one in tag_list:
            query = self.insert_tag(one)
            new_insert.append({"tag_id": query.id, "archive_id": self.id})
        Archive2Tag.insert_many(new_insert).execute()

    @tag.deleter
    def tag(self):
        archive2tag_query = Archive2Tag.delete().where(Archive2Tag.archive_id == self.id)
        archive2tag_query.execute()

    @property
    def author(self):
        user = User.select().where(User.id == self.user_id).first()
        return user

    def __repr__(self):
        return '<Archive({title!r})>'.format(title=self.title)


db.create_tables([Config, User, Archive, Tag, Archive2Tag], safe=True)
