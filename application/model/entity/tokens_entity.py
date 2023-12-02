from tortoise import fields
from tortoise.models import Model


class TokensEntity(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField(description="用户id", default=0)
    key = fields.CharField(max_length=155, description="key")
    status = fields.IntField(description="状态", default=1)
    name = fields.CharField(max_length=55, description="名称")
    created_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    expired_time = fields.DatetimeField(description="过期时间")

    class Meta:
        table = "tokens"
