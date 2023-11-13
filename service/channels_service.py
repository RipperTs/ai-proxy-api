import logging

from peewee import DoesNotExist

from common import config
from model.entity.channels_entity import ChannelsEntity
import requests

from model.po.add_channel_po import AddChannelPo


def get_base_url(channel):
    if channel['base_url'] is None or len(channel['base_url']) == 0:
        if channel['type'] == 1:
            return "https://api.openai.com"
        if channel['type'] == 2:
            return "https://api.ohmygpt.com"
        if channel['type'] == 4:
            return "https://api.openai-sb.com"
        else:
            logging.warning("渠道base_url为空")
    return channel.get('base_url','')


async def get_channel_info(model_name: str):
    channel = ChannelsEntity.get_by_model(model_name)
    if channel is None:
        raise Exception("渠道不存在")

    channel['base_url'] = get_base_url(channel)
    return channel


def get_channel_list(page=1, limit=30):
    result = ChannelsEntity.get_channel_list(page, limit)
    return result


def get_channel_balance(channel_id):
    balance = 0
    channel = ChannelsEntity.get_channel_by_id(channel_id)
    if channel['type'] == 2:
        req = requests.post("https://api.ohmygpt.com/api/v1/user/admin/balance",
                            headers={"authorization": "Bearer " + channel['key']},
                            timeout=15).json()
        if req['statusCode'] == 200:
            balance = int((float(req['data']['balance']) / 34000) * 100)

        # 更新渠道余额
        ChannelsEntity.update(balance=balance).where(ChannelsEntity.id == channel_id).execute()
    return balance


def do_add_channel(data: AddChannelPo):
    # 检查key 是否存在
    channel = ChannelsEntity.get_channel_by_key(data.key)
    if channel is not None:
        raise Exception("渠道key已存在")
    channel = ChannelsEntity()
    channel.key = data.key
    channel.type = data.type
    channel.name = data.name
    channel.base_url = data.base_url
    channel.models = data.models
    channel.save(force_insert=True)
    return channel


def do_del_channel(channel_id):
    # 检查key 是否存在
    channel = ChannelsEntity.get_channel_by_id(channel_id)
    if channel is None:
        raise Exception("渠道不存在")
    ChannelsEntity.delete_by_id(channel_id)
    return True


def do_change_channel_status(channel_id, status):
    # 检查key 是否存在
    channel = ChannelsEntity.get_channel_by_id(channel_id)
    if channel is None:
        raise Exception("渠道不存在")
    ChannelsEntity.update(status=status).where(ChannelsEntity.id == channel_id).execute()
    return True


def get_channel_by_id(channel_id):
    channel = ChannelsEntity.get_channel_by_id(channel_id)
    if channel is None:
        raise Exception("渠道不存在")
    channel['base_url'] = get_base_url(channel)
    return channel


def update_channel_response_time(channel_id, response_time):
    ChannelsEntity.update(response_time=response_time).where(ChannelsEntity.id == channel_id).execute()
    return True


def do_update_channel(channel_id, data: AddChannelPo):
    try:
        channel = ChannelsEntity.get_by_id(channel_id)
        channel.key = data.key
        channel.type = data.type
        channel.name = data.name
        channel.base_url = data.base_url
        channel.models = data.models
        channel.save()
        return channel
    except DoesNotExist:
        raise Exception("渠道不存在")


def get_channel_info_by_id(channel_id: int):
    try:
        channel = ChannelsEntity.get_by_id(channel_id)
        return channel.__dict__.get('__data__')
    except DoesNotExist:
        return None
