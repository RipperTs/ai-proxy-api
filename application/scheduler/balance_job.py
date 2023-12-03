import logging

from application.model.entity.channels_entity import ChannelsEntity
from application.service.channels_service import get_channel_balance


async def sync_balance():
    """
    同步渠道余额
    :return:
    """
    logging.info("开始同步渠道余额")

    channel_list = await ChannelsEntity.all()

    for channel in channel_list:
        try:
            await get_channel_balance(channel.id)
        except Exception as e:
            logging.error(e)
            continue

    logging.info("同步渠道余额结束")
