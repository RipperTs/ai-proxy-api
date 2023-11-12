from peewee import *
import datetime
from common import config

db = MySQLDatabase(config.db_database, host=config.db_host, user=config.db_user,
                   passwd=config.db_password,
                   port=int(config.db_port), charset='utf8')


class UsersEntity(Model):
    id = PrimaryKeyField()
    username = CharField()
    email = CharField()
    status = IntegerField(default=1)
    password = CharField()
    created_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        table_name = 'users'

    @classmethod
    def get_by_email(cls, email):
        try:
            result = cls.select().where(cls.email == email).dicts().get()
            return result
        except DoesNotExist:
            return None
        finally:
            db.close()

    @classmethod
    def add_user(cls, username, email, password, status=1):
        try:
            user = cls()
            user.username = username
            user.email = email
            user.password = password
            user.status = status
            user.save(force_insert=True)
            return user
        finally:
            db.close()
