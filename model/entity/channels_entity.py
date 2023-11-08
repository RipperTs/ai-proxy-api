from peewee import *
import datetime
from common import config

db = MySQLDatabase(config.db_database, host=config.db_host, user=config.db_user,
                   passwd=config.db_password,
                   port=int(config.db_port), charset='utf8')


class ChannelsEntity(Model):
    """
    渠道信息
    """
    id = PrimaryKeyField()
    type = IntegerField(default=1)
    key = CharField()
    status = IntegerField(default=1)
    name = CharField()
    weight = IntegerField(default=100)
    created_time = DateTimeField(default=datetime.datetime.now)
    test_time = DateTimeField()
    response_time = IntegerField(default=0)
    base_url = CharField()
    balance = IntegerField(default=0)
    balance_update_time = DateTimeField()
    models = CharField()
    used_quota = IntegerField(default=0)

    class Meta:
        database = db
        table_name = 'channels'

    @classmethod
    def get_by_model(self, model):
        """
        根据model随机获取渠道信息
        :param model:
        :return:
        """
        try:
            result = self.select().where(self.models.contains(model)).where(self.status == 1).order_by(
                fn.Rand()).dicts().limit(1)
            if len(result) > 0:
                return result[0]
            return None
        finally:
            db.close()

    @classmethod
    def get_channel_list(cls, page, limit):
        try:
            result = cls.select().order_by(cls.id.desc()).dicts().paginate(page, limit)
            return list(result)
        except DoesNotExist:
            return []
        finally:
            db.close()

    @classmethod
    def get_channel_by_id(cls, channel_id):
        try:
            result = cls.get_by_id(channel_id)
            # 返回字典类型
            return result.__dict__.get('__data__')
        except DoesNotExist:
            raise Exception("渠道不存在")
        finally:
            db.close()

    @classmethod
    def get_channel_by_key(self, key):
        try:
            result = self.select().where(self.key == key).dicts().get()
            return result
        except DoesNotExist:
            return None
        finally:
            db.close()


if __name__ == '__main__':
    print(ChannelsEntity.get_channel_by_id(2))
