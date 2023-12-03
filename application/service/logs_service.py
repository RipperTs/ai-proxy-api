import logging

from application.common import config
from application.model.entity.logs_entity import LogsEntity
from application.model.entity.tokens_entity import TokensEntity
from application.utils.tiktokens import num_tokens_from_string


async def get_log_list(page=1, limit=30):
    offset = (page - 1) * limit
    # 使用filter进行条件过滤，如果不需要过滤条件，则不调用filter
    query = LogsEntity.filter()
    # 使用offset和limit进行分页
    results = await query.offset(offset).order_by("-id").limit(limit).all()
    # 获取查询结果总数（用于分页）
    total_count = await query.count()
    for res in results:
        res.created_time = res.created_time.strftime('%Y-%m-%d %H:%M:%S')
    return results, total_count


async def insert_log(data: dict, model_name: str, channel: dict, token_info: TokensEntity):
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
