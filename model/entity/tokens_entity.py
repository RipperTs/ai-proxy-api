from peewee import *
import datetime
from common import config

db = MySQLDatabase(config.db_database, host=config.db_host, user=config.db_user,
                   passwd=config.db_password,
                   port=int(config.db_port), charset='utf8')


class TokensEntity(Model):
    id = PrimaryKeyField()
    user_id = IntegerField(default=0)
    key = CharField()
    status = IntegerField(default=1)
    name = CharField()
    created_time = DateTimeField(default=datetime.datetime.now)
    expired_time = DateTimeField()

    class Meta:
        database = db
        table_name = 'tokens'

    @classmethod
    def get_token_by_id(self, token_id):
        try:
            result = self.get_by_id(token_id)
            return result
        except DoesNotExist:
            return None
        finally:
            db.close()

    @classmethod
    async def get_by_key(self, key):
        """
        根据key获取token信息
        :param key:
        :return:
        """
        try:
            result = self.select().where(self.key == key).where(self.status == 1).dicts().get()
            return result
        except DoesNotExist:
            return None
        finally:
            db.close()

    @classmethod
    def get_token_list(self, page, limit):
        try:
            result = self.select().order_by(self.id.desc()).dicts().paginate(page, limit)
            return list(result)
        except DoesNotExist:
            return []
        finally:
            db.close()

    @classmethod
    def change_status(cls, token_id, status):
        try:
            result = cls.update(status=status).where(cls.id == token_id).execute()
            return result
        except DoesNotExist:
            return None
        finally:
            db.close()

    @classmethod
    def delete_token(self, token_id):
        try:
            return self.delete_by_id(token_id)
        finally:
            db.close()

    @classmethod
    def create_token(cls, key, name, status, user_id, expired_time):
        try:
            token = cls()
            token.key = key
            token.name = name
            token.status = status
            token.user_id = user_id
            token.expired_time = expired_time
            token.save(force_insert=True)
            return token
        finally:
            db.close()
