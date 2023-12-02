from fastapi import Request
import json

from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask

from application.common import config
import logging
import httpx
import tenacity

from application.service.channels_service import get_channel_info
from application.service.logs_service import insert_log
from application.service.token_service import get_token_info

client = httpx.AsyncClient()
logger = logging.getLogger(__name__)


@tenacity.retry(wait=tenacity.wait_fixed(1), stop=tenacity.stop_after_attempt(5), reraise=True,
                retry=tenacity.retry_if_exception_type(Exception),
                before_sleep=tenacity.before_sleep_log(logger, logging.WARNING))
async def do_openai_proxy(request: Request):
    """
    OpenAI转发代理请求操作
    :param request: 请求对象
    :return: StreamingResponse
    """
    url_path = request.url.path
    headers = dict(request.headers)
    token_info = await get_token_info(headers['authorization'])
    # 获取请求的参数
    data = request.state.request_data
    stream = data.get('stream', False)
    model_name = data.get('model', '')

    if model_name is None or len(model_name) == 0:
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
        data['model'] = config.azure_chat_model

    logging.warning(
        f"代理请求: {channel['base_url']}{url_path}, 模型: {model_name}, azure: {config.use_azure_model}")
    req = client.build_request(
        method=request.method,
        url=f"{channel['base_url']}{url_path}",
        headers=headers,
        content=json.dumps(data).encode('utf-8') if "application/json" in headers.get('content-type',
                                                                                      '') else data,
        cookies=request.cookies,
        timeout=120.0 if stream else 600.0
    )
    r = await client.send(req, stream=True, follow_redirects=False)

    # 记录请求日志
    await insert_log(data.get('messages', []), model_name, channel, token_info)
    return StreamingResponse(r.aiter_raw(), background=BackgroundTask(r.aclose),
                             status_code=r.status_code, headers=dict(r.headers), media_type='text/event-stream')
