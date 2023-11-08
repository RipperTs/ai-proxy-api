from model.entity.logs_entity import LogsEntity
from utils.tiktokens import num_tokens_from_string


async def insert_log(messages: list, model_name: str, channel, token_info):
    """
    记录日志
    :param messages:
    :param model_name:
    :param channel:
    :param token_info:
    :return:
    """
    content = ''
    for message in messages:
        content += message['content']

    token_num = num_tokens_from_string(content)
    LogsEntity.insert_log('', token_info['name'], model_name, channel['id'], channel['name'], request_tokens=token_num)


def get_log_list(page=1, limit=30):
    result = LogsEntity.get_log_list(page, limit)
    return result
