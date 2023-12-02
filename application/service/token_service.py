import datetime
import re

from application.model.entity.tokens_entity import TokensEntity
from application.model.po.add_token_po import AddTokenPo
from application.utils.tiktokens import generate_random_string


async def get_token_info(bearer_token) -> TokensEntity:
    token_with_sk = re.search(r'Bearer (.+)', bearer_token).group(1)
    token_without_sk = token_with_sk.replace("sk-", "")

    token_query = TokensEntity.filter(key=token_without_sk)

    token_exists = await token_query.exists()
    if token_exists is False:
        raise AssertionError("鉴权失败: 令牌不存在")

    token_info = await token_query.first()
    if token_info.expired_time is not None:
        # 获取现在时间
        now = datetime.datetime.now()
        expired_time = token_info.expired_time
        if now > expired_time:
            raise AssertionError("鉴权失败: 令牌已过期")

    return token_info


async def get_token_list(page=1, limit=30):
    offset = (page - 1) * limit
    query = TokensEntity.filter()
    results = await query.offset(offset).order_by("-id").limit(limit).all()
    total_count = await query.count()
    for item in results:
        item.key = f"sk-{item.key}"
        item.created_time = item.created_time.strftime('%Y-%m-%d %H:%M:%S')
        item.expired_time = item.expired_time.strftime('%Y-%m-%d %H:%M:%S') if item.expired_time is not None else None

    return results, total_count


async def do_add_token(data: AddTokenPo):
    key = generate_random_string(48)
    token = TokensEntity(key=key, name=data.name, status=data.status, user_id=data.user_id,
                         expired_time=data.expired_time)
    await token.save()
    return token.id


async def do_del_token(token_id: int):
    query = TokensEntity.filter(id=token_id)
    token_exists = await query.exists()
    if token_exists is False:
        raise AssertionError("令牌不存在")
    return await query.delete()


async def do_change_token_status(token_id: int, status: int):
    query = TokensEntity.filter(id=token_id)
    token_exists = await query.exists()
    if token_exists is False:
        raise AssertionError("令牌不存在")

    return await query.update(status=status)


async def do_update_token(token_id: int, data: AddTokenPo):
    query = TokensEntity.filter(id=token_id)
    token_exists = await query.exists()
    if token_exists is False:
        raise AssertionError("令牌不存在")

    token = await query.first()
    token.name = data.name
    token.expired_time = data.expired_time
    await token.save()
    return token.id


async def get_token_info_by_id(token_id: int):
    query = TokensEntity.filter(id=token_id)
    token_exists = await query.exists()
    if token_exists is False:
        raise AssertionError("令牌不存在")

    token = await query.first()
    return token
