import logging

import requests
from fastapi import FastAPI, Form
from common import config
from common.vo import resultSuccess, resultError
from handler.exception_handler import register_all_handler
from model.po.add_channel_po import AddChannelPo
from model.po.add_token_po import AddTokenPo
from model.po.register_user_po import RegisterUserPo
from service.channels_service import get_channel_list, get_channel_balance, do_add_channel, \
    do_del_channel, do_change_channel_status, get_channel_by_id, update_channel_response_time
from service.logs_service import get_log_list
from service.token_service import get_token_list, do_add_token, do_del_token, \
    do_change_token_status
import time

from service.users_sercice import create_user

app = FastAPI()
register_all_handler(app)


@app.get('/ai-proxy/api/log-list')
def log_list(page: int = 1, limit: int = 30):
    result = get_log_list(page, limit)
    return resultSuccess(data=result)


@app.get('/ai-proxy/api/channel-list')
def channel_list(page: int = 1, limit: int = 30):
    result = get_channel_list(page, limit)
    return resultSuccess(data=result)


@app.get('/ai-proxy/api/token-list')
def token_list(page: int = 1, limit: int = 30):
    result = get_token_list(page, limit)
    return resultSuccess(data=result)


@app.get('/ai-proxy/api/balance')
def balance(channel_id):
    try:
        result = get_channel_balance(channel_id)
        return resultSuccess(data={"balance": result / 100})
    except Exception as e:
        return resultError(msg=str(e))


@app.post('/ai-proxy/api/add-channel')
def add_channel(data: AddChannelPo):
    try:
        result = do_add_channel(data)
        return resultSuccess(data=result)
    except Exception as e:
        return resultError(msg=str(e))


@app.post('/ai-proxy/api/{channel_id}/del-channel')
def del_channel(channel_id: int):
    try:
        do_del_channel(channel_id)
        return resultSuccess(data={})
    except Exception as e:
        return resultError(msg=str(e))


@app.get('/ai-proxy/api/channel/{channel_id}/status')
def change_channel_status(channel_id: int, status: int):
    try:
        do_change_channel_status(channel_id, status)
        return resultSuccess(data={})
    except Exception as e:
        return resultError(msg=str(e))


@app.post('/ai-proxy/api/add-token')
def add_token(data: AddTokenPo):
    try:
        result = do_add_token(data)
        return resultSuccess(data=result)
    except Exception as e:
        return resultError(msg=str(e))


@app.post('/ai-proxy/api/{token_id}/del-token')
def del_token(token_id: int):
    try:
        do_del_token(token_id)
        return resultSuccess(data={})
    except Exception as e:
        return resultError(msg=str(e))


@app.get('/ai-proxy/api/token/{token_id}/status')
def change_token_status(token_id: int, status: int):
    do_change_token_status(token_id, status)
    return resultSuccess(data={})


@app.get('/ai-proxy/api/check-channel')
def check_channel(channel_id: int):
    try:
        channel = get_channel_by_id(channel_id)
        test_request_data = {'messages': [{'role': 'user', 'content': 'Hello!'}],
                             'stream': False}
        test_request_data['model'] = channel['models'].split(',')[0]
        headers = {'content-type': 'application/json', 'authorization': f"Bearer {channel['key']}"}
        # 记录开始时间
        start_time = time.time()
        response = requests.request(
            method='post',
            url=f"{channel['base_url']}/v1/chat/completions",
            headers=headers,
            json=test_request_data,
            allow_redirects=False,
            timeout=10)
        # 计算响应时间, 单位ms
        response_time = int((time.time() - start_time) * 1000)
        update_channel_response_time(channel_id, response_time)
        if response.status_code != 200:
            raise Exception(f"请求失败, {response.text}")
        return resultSuccess(data={
            "response_time": response_time,
            "response": response.json()
        })

    except Exception as e:
        logging.error(f"检测渠道失败, {e}")
        return resultError(msg=str(e))


@app.post('/ai-proxy/api/register-user', )
def register_user(data: RegisterUserPo):
    try:
        user = create_user(data.username, data.email, data.password)
        return resultSuccess(data=user, msg="注册成功, 无法自动登录, 请联系管理员验证账号后登录")
    except Exception as e:
        return resultError(msg=str(e))


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='app:app', host=config.server_name, port=config.server_port, workers=2, reload=False)
