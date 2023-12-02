from fastapi import APIRouter

from application.common.vo import resultSuccess
from application.model.entity.channels_entity import ChannelsEntity
from application.model.po.add_channel_po import AddChannelPo
from application.service.channels_service import get_channel_list, get_channel_balance, do_add_channel, do_del_channel, \
    do_change_channel_status, do_check_channel, do_update_channel, get_channel_info

router = APIRouter()


@router.get('/channel-list')
async def channel_list(page: int = 1, limit: int = 30):
    """
    获取渠道列表
    :param page:
    :param limit:
    :return:
    """
    results, total_count = await get_channel_list(page, limit)
    return resultSuccess(data={
        "list": results,
        "total_count": total_count
    })


@router.get('/balance')
async def balance(channel_id: int):
    """
    更新渠道余额
    :param channel_id:
    :return:
    """
    result = await get_channel_balance(channel_id)
    return resultSuccess(data={"balance": result / 100})


@router.post('/add-channel')
async def add_channel(data: AddChannelPo):
    """
    添加渠道
    :param data:
    :return:
    """
    result = await do_add_channel(data)
    return resultSuccess(data=result)


@router.post('/{channel_id}/del-channel')
async def del_channel(channel_id: int):
    """
    删除渠道
    :param channel_id:
    :return:
    """
    result = await do_del_channel(channel_id)
    return resultSuccess(data=result)


@router.get('/{channel_id}/status')
async def change_channel_status(channel_id: int, status: int):
    """
    修改渠道状态
    :param channel_id:
    :param status:
    :return:
    """
    result = await do_change_channel_status(channel_id, status)
    return resultSuccess(data=result)


@router.get('/check-channel')
async def check_channel(channel_id: int):
    """
    检查渠道是否可用
    :param channel_id:
    :return:
    """
    result = await do_check_channel(channel_id)
    return resultSuccess(data=result)


@router.post('/{channel_id}/update-channel')
async def update_channel(channel_id: int, data: AddChannelPo):
    """
    更新渠道
    :param channel_id:
    :param data:
    :return:
    """
    result = await do_update_channel(channel_id, data)
    return resultSuccess(data=result)


@router.get('/channel-info')
async def channel_info(channel_id: int):
    """
    获取渠道信息
    :param channel_id:
    :return:
    """
    result = await ChannelsEntity.filter(id=channel_id).first()
    return resultSuccess(data=result)


@router.get('/test-random-channel')
async def test_random_channel(model_name: str):
    """
    随机获取一个可用的渠道
    :return:
    """
    result = await get_channel_info(model_name)
    return resultSuccess(data=result)
