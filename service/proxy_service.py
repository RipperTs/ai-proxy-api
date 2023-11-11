from fastapi import Request
import json

from fastapi.responses import StreamingResponse, Response
from starlette.background import BackgroundTask

from common import config
from service.channels_service import get_channel_info
from service.logs_service import insert_log
from service.token_service import get_token_info
import logging
import httpx

client = httpx.AsyncClient()


async def do_proxy(request: Request):
    try:
        url_path = request.url.path
        headers = dict(request.headers)
        token_info = await get_token_info(headers['authorization'])
        # 获取请求的参数
        if "application/json" in headers['content-type']:
            data = await request.json()
        else:
            data = await request.form()
            data = dict(data)

        stream = data.get('stream', False)
        model_name = data.get('model', '')

        if model_name is None or len(model_name) == 0:
            logging.error("model参数不能为空")
            raise Exception("model参数不能为空")

        # 获取渠道信息
        channel = await get_channel_info(model_name)
        if 'host' in headers:
            del headers['host']
        if 'content-length' in headers:
            del headers['content-length']
        # 设置代理请求头(openai的接口鉴权sk-xxx需要填写在这里)
        headers['authorization'] = f"Bearer {channel['key']}"

        # 如果使用azure模型, 则将请求路径修改为azure的路径
        if config.use_azure_model:
            if url_path == '/v1/chat/completions':
                url_path = '/azure/v1/chat/completions'
            # 修改data中的model参数
            data['model'] = config.azure_chat_model

        logging.warning(f"代理请求: {channel['base_url']}{url_path}, 模型: {model_name}, azure: {config.use_azure_model}")
        req = client.build_request(
            method=request.method,
            url=f"{channel['base_url']}{url_path}",
            headers=headers,
            content=json.dumps(data).encode('utf-8') if "application/json" in headers.get('content-type',
                                                                                          '') else data,
            cookies=request.cookies,
            timeout=20.0 if stream else 300.0
        )
        r = await client.send(req, stream=True)
        if r.status_code != 200:
            raise Exception(f"请求失败, 状态码: {r.status_code}")

        await insert_log(data.get('messages', []), model_name, channel, token_info)
        return StreamingResponse(r.aiter_raw(), background=BackgroundTask(r.aclose),
                                 status_code=r.status_code, headers=dict(r.headers), media_type='text/event-stream')

    except Exception as e:
        logging.error(f"代理转发请求失败, 错误信息: {e}")
        return Response(json.dumps({"code": 500, "data": None, "message": str(e)}), status_code=200)
