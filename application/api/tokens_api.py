from fastapi import APIRouter

from application.common.vo import resultSuccess
from application.model.po.add_token_po import AddTokenPo
from application.service.token_service import get_token_list, do_add_token, do_del_token, do_change_token_status, \
    do_update_token, get_token_info_by_id

router = APIRouter()


@router.get('/token-list')
async def token_list(page: int = 1, limit: int = 30):
    """
    获取token列表
    :param page:
    :param limit:
    :return:
    """
    results, total_count = await get_token_list(page, limit)
    return resultSuccess(data={
        "list": results,
        "total_count": total_count
    })


@router.post('/add-token')
async def add_token(data: AddTokenPo):
    """
    添加token
    :param data:
    :return:
    """
    result = await do_add_token(data)
    return resultSuccess(data=result)


@router.post('/{token_id}/del-token')
async def del_token(token_id: int):
    """
    删除token
    :param token_id:
    :return:
    """
    result = await do_del_token(token_id)
    return resultSuccess(data=result)


@router.get('/{token_id}/status')
async def change_token_status(token_id: int, status: int):
    """
    修改token状态
    :param token_id:
    :param status:
    :return:
    """
    result = await do_change_token_status(token_id, status)
    return resultSuccess(data=result)


@router.post('/{token_id}/update-token')
async def update_token(token_id: int, data: AddTokenPo):
    """
    修改token
    :param token_id:
    :param data:
    :return:
    """
    result = await do_update_token(token_id, data)
    return resultSuccess(data=result)


@router.get('/token-info')
async def token_info(token_id: int):
    """
    获取token详情
    :param token_id:
    :return:
    """
    result = await get_token_info_by_id(token_id)
    return resultSuccess(data=result)
