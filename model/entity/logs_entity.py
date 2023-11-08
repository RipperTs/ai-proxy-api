from peewee import *
import datetime
from common import config

db = MySQLDatabase(config.db_database, host=config.db_host, user=config.db_user,
                   passwd=config.db_password,
                   port=int(config.db_port), charset='utf8')


class LogsEntity(Model):
    id = PrimaryKeyField()
    type = IntegerField(default=1)
    content = CharField()
    token_name = CharField()
    model_name = CharField()
    request_tokens = IntegerField(default=0)
    channel_id = IntegerField(default=0)
    channel_name = CharField()
    created_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        table_name = 'logs'

    @classmethod
    def insert_log(self, content, token_name, model_name, channel_id, channel_name, **kwargs):
        try:
            return self.create(content=content, token_name=token_name, model_name=model_name, channel_id=channel_id,
                               channel_name=channel_name, **kwargs)
        finally:
            db.close()

    @classmethod
    def get_log_list(self, page=1, limit=30):
        try:
            result = self.select().order_by(self.id.desc()).dicts().paginate(page, limit)
            return list(result)
        except DoesNotExist:
            return []
        finally:
            db.close()


if __name__ == '__main__':
    print(LogsEntity.get_log_list(1))
