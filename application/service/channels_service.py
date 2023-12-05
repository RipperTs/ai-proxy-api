import logging

from peewee import DoesNotExist

from application.model.entity.channels_entity import ChannelsEntity
import httpx
import time

from application.model.po.add_channel_po import AddChannelPo

import random


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
    return channel.get('base_url', '')


async def get_channel_info(model_name: str) -> dict:
    if model_name == '':
        raise AssertionError("模型名称不能为空")
    channel_list = await ChannelsEntity.random_channel_by_model_name(model_name)
    if len(channel_list) == 0:
        raise AssertionError("未找到可用的渠道")
    # 按权重随机选择一个渠道
    channel = random.choices(channel_list, weights=[channel['weight'] for channel in channel_list])[0]
    channel['base_url'] = get_base_url(channel)
    return channel


async def get_channel_list(page=1, limit=30):
    offset = (page - 1) * limit
    query = ChannelsEntity.filter()
    results = await query.offset(offset).order_by("-id").limit(limit).all()
    total_count = await query.count()
    for res in results:
        res.created_time = res.created_time.strftime('%Y-%m-%d %H:%M:%S')
        if res.balance_update_time not in ['', None]:
            res.balance_update_time = res.balance_update_time.strftime('%Y-%m-%d %H:%M:%S')
    return results, total_count


async def get_channel_balance(channel_id: int):
    """
    获取渠道余额
    :param channel_id:
    :return:
    """
    balance = 0
    query = ChannelsEntity.filter(id=channel_id)

    channel_exists = await query.exists()
    if channel_exists is False:
        raise AssertionError("渠道不存在")

    channel = await query.first()
    if channel.type == 2:
        # ohmygpt
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{get_base_url(channel.__dict__)}/api/v1/user/admin/balance",
                                         headers={"authorization": "Bearer " + channel.key}, timeout=20)
            if response.status_code != 200:
                raise AssertionError(
                    f"获取渠道余额失败, 请求状态码: {response.status_code}, 错误信息: {response.aread()}")

            response_json = response.json()
            if response_json['statusCode'] != 200:
                raise AssertionError(f"获取渠道余额失败, 错误信息: {response_json['message']}")
            balance = int((float(response_json['data']['balance']) / 34000) * 100)

    if channel.type == 3:
        #  One API
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{get_base_url(channel.__dict__)}/api/status", timeout=20)
            if response.status_code != 200:
                raise AssertionError(
                    f"获取渠道余额失败, 请求状态码: {response.status_code}, 错误信息: {response.aread()}")
            response_json = response.json()
            quota_per_unit = response_json['data']['quota_per_unit']

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{get_base_url(channel.__dict__)}/api/user/self", headers={
                'authorization': 'Bearer ' + channel.manage_key,
            }, timeout=20)
            if response.status_code != 200:
                raise AssertionError(
                    f"获取渠道余额失败, 请求状态码: {response.status_code}, 错误信息: {response.aread()}")
            response_json = response.json()
            quota = response_json['data']['quota']

        balance = int(round((quota / quota_per_unit), 2) * 100)

    if channel.type == 4:
        # openai-sb
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{get_base_url(channel.__dict__)}/sb-api/user/status?api_key={channel.key}",
                                        timeout=20)
            if response.status_code != 200:
                raise AssertionError(
                    f"获取渠道余额失败, 请求状态码: {response.status_code}, 错误信息: {response.aread()}")
            response_json = response.json()
            balance = int(float(response_json['data']['credit'])) / 100

    # 获取当前时间 格式 yyyy-MM-dd HH:mm:ss
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    await query.update(balance=balance, balance_update_time=now)
    return balance


async def do_add_channel(data: AddChannelPo):
    # 检查key 是否存在
    channel_exists = await ChannelsEntity.filter(key=data.key).exists()
    if channel_exists:
        raise AssertionError("渠道key已存在")
    channel = ChannelsEntity(key=data.key, type=data.type, name=data.name, base_url=data.base_url, models=data.models)
    await channel.save()
    return channel.id


async def do_del_channel(channel_id: int):
    channel_exists = await ChannelsEntity.filter(id=channel_id).exists()
    if channel_exists is False:
        raise AssertionError("渠道不存在")
    return await ChannelsEntity.filter(id=channel_id).delete()


async def do_change_channel_status(channel_id: int, status: int):
    channel_exists = await ChannelsEntity.filter(id=channel_id).exists()
    if channel_exists is False:
        raise AssertionError("渠道不存在")
    return await ChannelsEntity.filter(id=channel_id).update(status=status)


async def do_check_channel(channel_id: int):
    channel_exists = await ChannelsEntity.filter(id=channel_id).exists()
    if channel_exists is False:
        raise AssertionError("渠道不存在")

    channel = await ChannelsEntity.filter(id=channel_id).first()
    test_request_data = {'messages': [{'role': 'user', 'content': 'Hello!'}],
                         'stream': False}
    test_request_data['model'] = channel.models.split(',')[0]
    headers = {'content-type': 'application/json', 'authorization': f"Bearer {channel.key}"}
    # 记录开始时间
    start_time = time.time()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{get_base_url(channel.__dict__)}/v1/chat/completions", headers=headers,
                                     json=test_request_data, timeout=10)
        if response.status_code != 200:
            raise AssertionError(f"请求失败: {response.text}")

        # 计算响应时间, 单位ms
        response_time = int((time.time() - start_time) * 1000)
        await update_channel_response_time(channel_id, response_time)
        return {
            "response_time": response_time,
            "response": response.json()
        }


async def update_channel_response_time(channel_id: int, response_time: int):
    await ChannelsEntity.filter(id=channel_id).update(response_time=response_time)
    return True


async def do_update_channel(channel_id: int, data: AddChannelPo):
    channel_exists = await ChannelsEntity.filter(id=channel_id).exists()
    if channel_exists is False:
        raise AssertionError("渠道不存在")

    channel = await ChannelsEntity.filter(id=channel_id).first()
    channel.key = data.key
    channel.type = data.type
    channel.name = data.name
    channel.base_url = data.base_url
    channel.models = data.models
    await channel.save()
    return channel.id
