from tortoise import fields
from tortoise.models import Model


class LogsEntity(Model):
    id = fields.IntField(pk=True)
    type = fields.IntField(description="类型", default=1)
    content = fields.TextField(description="内容")
    token_name = fields.CharField(max_length=55, description="token名称")
    model_name = fields.CharField(max_length=55, description="模型名称")
    request_tokens = fields.IntField(description="请求token数量", default=0)
    channel_id = fields.IntField(description="渠道id", default=0)
    channel_name = fields.CharField(max_length=55, description="渠道名称")
    created_time = fields.DatetimeField(auto_now_add=True, description="创建时间")

    class Meta:
        table = "logs"
