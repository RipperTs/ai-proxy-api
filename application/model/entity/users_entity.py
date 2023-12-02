from tortoise import fields
from tortoise.models import Model


class UsersEntity(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=55, description="用户名")
    email = fields.CharField(max_length=100, description="邮箱")
    status = fields.IntField(description="状态", default=1)
    password = fields.CharField(max_length=155, description="密码")
    created_time = fields.DatetimeField(auto_now_add=True, description="创建时间")

    class Meta:
        table = "users"
