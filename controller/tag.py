class TagHandle(object):
    def __init__(self, archive_id):
        self.archive_id = archive_id

    @staticmethod
    def tag_exist(name):
        from database import Tag
        query = Tag.select().where(Tag.content == name).first()
        return query if query else False

    def insert_tag(self, name):
        from database import Tag
        query = self.tag_exist(name)
        if not query:
            query = Tag()
            query.content = name
            query.save()
        return query

    def tag_text(self):
        tag_list = self.tag
        result = ""
        if len(tag_list) > 0:
            result = tag_list[0]
        for i in range(1, len(tag_list)):
            result += ",{}".format(tag_list[i])
        return result

    @property
    def tag(self):
        from database import Archive2Tag, Tag
        query = Archive2Tag.select(Archive2Tag.tag_id).where(Archive2Tag.archive_id == self.archive_id)
        tag_ids = [one.tag_id for one in query]
        tag_query = Tag.select(Tag.content).where(Tag.id << tag_ids) if len(tag_ids) > 0 else []
        return [one.content for one in tag_query]

    @tag.setter
    def tag(self, tag_list):
        from database import Archive2Tag
        tag_list = tag_list.split(" ")
        archive2tag_query = Archive2Tag.delete().where(Archive2Tag.archive_id == self.archive_id)
        archive2tag_query.execute()
        new_insert = []
        for one in tag_list:
            query = self.insert_tag(one)
            new_insert.append({"tag_id": query.id, "archive_id": self.archive_id})
        Archive2Tag.insert_many(new_insert).execute()

    @tag.deleter
    def tag(self):
        from database import Archive2Tag
        archive2tag_query = Archive2Tag.delete().where(Archive2Tag.archive_id == self.archive_id)
        archive2tag_query.execute()
