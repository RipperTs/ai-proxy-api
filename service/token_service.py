import datetime
import re

from model.entity.tokens_entity import TokensEntity
from model.po.add_token_po import AddTokenPo
from utils.tiktokens import generate_random_string


async def get_token_info(bearer_token):
    token_with_sk = re.search(r'Bearer (.+)', bearer_token).group(1)
    token_without_sk = token_with_sk.replace("sk-", "")
    token_info = TokensEntity.get_by_key(token_without_sk)
    if token_info is None:
        raise Exception("鉴权失败: 令牌不存在")

    if token_info['expired_time'] is not None:
        # 获取现在时间
        now = datetime.datetime.now()
        expired_time = token_info['expired_time']
        if now > expired_time:
            raise Exception("鉴权失败: 令牌已过期")

    return token_info


def get_token_list(page=1, limit=30):
    result = TokensEntity.get_token_list(page, limit)
    for item in result:
        item['key'] = f"sk-{item['key']}"
    return result


def do_add_token(data: AddTokenPo):
    key = generate_random_string(48)
    token = TokensEntity()
    token.key = key
    token.name = data.name
    token.status = data.status
    token.user_id = data.user_id
    token.expired_time = data.expired_time
    token.save(force_insert=True)
    return token


def do_del_token(token_id):
    return TokensEntity.delete_by_id(token_id)


def do_change_token_status(token_id, status):
    return TokensEntity.update(status=status).where(TokensEntity.id == token_id).execute()
