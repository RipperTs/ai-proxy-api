import requests
from fastapi import FastAPI, Request
import json

from fastapi.responses import StreamingResponse, Response

from common import config
from common.vo import resultSuccess, resultError
from handler.exception_handler import register_all_handler
from model.po.add_channel_po import AddChannelPo
from model.po.add_token_po import AddTokenPo
from service.channels_service import get_channel_info, get_channel_list, get_channel_balance, do_add_channel, \
    do_del_channel, do_change_channel_status
from service.logs_service import insert_log, get_log_list
from service.token_service import get_token_info, get_token_list, do_add_token, do_del_token, \
    do_change_token_status

app = FastAPI()
register_all_handler(app)


@app.middleware("http")
async def proxy(request: Request, call_next):
    if request.url.path.startswith("/ai-proxy"):
        return await call_next(request)
    try:
        headers = dict(request.headers)
        token_info = get_token_info(headers['authorization'])
        # 获取body中的参数
        data = await request.body()
        # 将字节类型的data转换为json
        data = json.loads(data)
        stream = data.get('stream', False)
        model_name = data.get('model', '')

        if model_name is None or len(model_name) == 0:
            raise Exception("model参数不能为空")

        # 获取渠道信息
        channel = get_channel_info(model_name)
        if 'host' in headers:
            del headers['host']
        # 设置代理请求头(openai的接口鉴权sk-xxx需要填写在这里)
        headers['authorization'] = f"Bearer {channel['key']}"
        # 记录请求日志, 异步调用insert_log方法
        await insert_log(data.get('messages', []), model_name, channel, token_info)
        # 发送代理请求
        response = requests.request(
            method=request.method,
            url=f"{channel['base_url']}{request.url.path}",
            headers=headers,
            json=data,
            cookies=request.cookies,
            allow_redirects=False,
            stream=stream,
            timeout=15)

        if response.status_code != 200:
            raise Exception("请求失败")

        if stream:
            # 流式返回结果
            return StreamingResponse(response.iter_content(chunk_size=1024), status_code=response.status_code,
                                     headers=dict(response.headers), media_type='text/event-stream')
        else:
            return Response(response.content, status_code=response.status_code, headers=dict(response.headers))
    except Exception as e:
        return Response(json.dumps({"code": 500, "data": None, "message": str(e)}), status_code=200)


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


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host=config.server_name, port=config.server_port)
