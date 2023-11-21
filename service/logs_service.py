import logging

from common import config
from model.entity.logs_entity import LogsEntity
from utils.tiktokens import num_tokens_from_string
import threading


def insert_log_thread(messages, model_name, channel, token_info):
    try:
        content = ''
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
        LogsEntity.insert_log(remark, token_info['name'], model_name, channel['id'], channel['name'],
                              request_tokens=token_num)
    except Exception as e:
        logging.error(f"新增请求日志失败: {e},  {model_name}, {channel}, {token_info}")
        return None


async def insert_log(messages: list, model_name: str, channel, token_info):
    thread = threading.Thread(target=insert_log_thread, args=(messages, model_name, channel, token_info))
    thread.start()


def get_log_list(page=1, limit=30):
    result = LogsEntity.get_log_list(page, limit)
    return result
