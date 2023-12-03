import logging

from application.common import config
from application.model.entity.logs_entity import LogsEntity
from application.model.entity.tokens_entity import TokensEntity
from application.utils.tiktokens import num_tokens_from_string


async def get_log_list(page: int = 1, limit: int = 30):
    """
    获取日志列表
    :param page:
    :param limit:
    :return:
    """
    offset = (page - 1) * limit
    query = LogsEntity.filter()
    results = await query.offset(offset).order_by("-id").limit(limit).all()
    total_count = await query.count()
    for res in results:
        res.created_time = res.created_time.strftime('%Y-%m-%d %H:%M:%S')
    return results, total_count


async def insert_log(data: dict, model_name: str, channel: dict, token_info: TokensEntity):
    """
    新增请求日志
    :param data:
    :param model_name:
    :param channel:
    :param token_info:
    :return:
    """
    try:
        content = ''
        messages = data.get('messages', [])
        input = data.get('input', '')
        if len(messages) == 0:
            content = input

        for message in messages:
            if isinstance(message['content'], str):
                content += message['content']
            elif isinstance(message['content'], list):
                for item in message['content']:
                    content += item.get('text', '')

        token_num = num_tokens_from_string(content)

        remark = ""
        if config.use_azure_model:
            remark = f"Azure OpenAI {config.azure_chat_model}"

        await LogsEntity.create(content=remark, token_name=token_info.name, model_name=model_name,
                                request_tokens=token_num, channel_id=channel['id'], channel_name=channel['name'])
    except Exception as e:
        logging.error(f"新增请求日志失败: {e},  {model_name}, {channel}, {token_info}")
        return None
