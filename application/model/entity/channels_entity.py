from typing import List

from tortoise import fields, Tortoise
from tortoise.models import Model


class ChannelsEntity(Model):
    id = fields.IntField(pk=True)
    type = fields.IntField(description="类型", default=1)
    key = fields.CharField(max_length=55, description="key")
    status = fields.IntField(description="状态", default=1)
    name = fields.CharField(max_length=55, description="名称", default="")
    weight = fields.IntField(description="权重", default=1)
    created_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    test_time = fields.DatetimeField(description="测试时间")
    response_time = fields.IntField(description="响应时间", default=0)
    base_url = fields.CharField(max_length=255, description="base url")
    balance = fields.IntField(description="余额", default=0)
    balance_update_time = fields.DatetimeField(description="余额更新时间", default="1970-01-01 00:00:00")
    models = fields.CharField(max_length=550, description="模型", default="")
    used_quota = fields.IntField(description="已使用额度", default=0)
    manage_key = fields.CharField(max_length=155, description="管理key", default='')

    class Meta:
        table = "channels"

    @classmethod
    async def random_channel_by_model_name(cls, model_name: str) -> List[dict]:
        db = Tortoise.get_connection("default")
        result = await db.execute_query_dict(
            "select `id`,`key`,`type`,`name`,`status`,`weight`,`base_url`,`models`,`used_quota`,`balance` from channels WHERE FIND_IN_SET(%s,models) AND status = 1",
            [model_name])
        return result
