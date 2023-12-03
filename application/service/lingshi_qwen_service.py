import json
import time
from http import HTTPStatus

from pydantic import BaseModel, Field
from fastapi import HTTPException
from typing import List, Literal, Optional, Union
from sse_starlette.sse import EventSourceResponse
from dashscope import Generation
from fastapi import Request
import logging

from starlette.responses import Response

import tenacity

from application.service.channels_service import get_channel_info
from application.service.logs_service import insert_log
from application.service.token_service import get_token_info

logger = logging.getLogger(__name__)

class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class DeltaMessage(BaseModel):
    role: Optional[Literal["user", "assistant", "system"]] = None
    content: Optional[str] = None


class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Literal["stop", "length"]


class ChatCompletionResponseStreamChoice(BaseModel):
    index: int
    delta: DeltaMessage
    finish_reason: Optional[Literal["stop", "length"]]


class ChatCompletionResponse(BaseModel):
    model: str
    object: Literal["chat.completion", "chat.completion.chunk"]
    choices: List[Union[ChatCompletionResponseChoice, ChatCompletionResponseStreamChoice]]
    created: Optional[int] = Field(default_factory=lambda: int(time.time()))


@tenacity.retry(wait=tenacity.wait_fixed(1), stop=tenacity.stop_after_attempt(3), reraise=True,
                retry=tenacity.retry_if_exception_type(Exception),
                before_sleep=tenacity.before_sleep_log(logger, logging.WARNING))
async def do_lingshi_qwen_proxy(request: Request):
    global model, tokenizer

    data = request.state.request_data
    messages = request.state.request_data.get('messages', [])
    headers = dict(request.headers)
    token_info = await get_token_info(headers['authorization'])

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

    stream = data.get('stream', False)
    if messages[-1]['role'] != "user":
        raise HTTPException(status_code=400, detail="The `user` field was not found.")
    query = messages[-1]['content']

    prev_messages = messages[:-1]
    if stream:
        generate = predict(query,prev_messages, model_name, channel['key'], data.get('temperature', 0.5),
                           data.get('top_p', 0.9))
        # 记录请求日志
        await insert_log(data, model_name, channel, token_info)
        return EventSourceResponse(generate, media_type="text/event-stream")

    responses = Generation.call(
        model=model_name,
        seed=1234,
        prompt=query,
        api_key=channel['key'],
        temperature=data.get('temperature', 0.5),
        top_p=data.get('top_p', 0.9),
        max_length=1500
    )
    result = json.dumps(responses.output.text, indent=4, ensure_ascii=False)
    choice_data = ChatCompletionResponseChoice(
        index=0,
        message=ChatMessage(role="assistant", content=result),
        finish_reason="stop"
    )

    # 记录请求日志
    await insert_log(data, model_name, channel, token_info)
    model_result = ChatCompletionResponse(model=model_name, choices=[choice_data], object="chat.completion")
    return Response(model_result.model_dump_json(exclude_unset=True), media_type="application/json")


async def predict(query,messages, model_name: str, api_key: str, temperature: float = 0.5,
                  top_p: float = 0.9):
    choice_data = ChatCompletionResponseStreamChoice(
        index=0,
        delta=DeltaMessage(role="assistant"),
        finish_reason=None
    )
    chunk = ChatCompletionResponse(model=model_name, choices=[choice_data], object="chat.completion.chunk")
    yield "{}".format(chunk.model_dump_json(exclude_unset=True))

    responses = Generation.call(
        prompt=query,
        model=model_name,
        messages=messages,
        api_key=api_key,
        seed=1234,
        stream=True,
        temperature=temperature,
        top_p=top_p,
        max_length=1500,
        enable_search=True,
    )
    current_length = 0
    for response in responses:
        if response.status_code != HTTPStatus.OK:
            new_text = "出错了, 错误码: {}, 请求ID: {}, 信息: {}".format(response.status_code, response.request_id,
                                                                         response.message)
            logger.error(new_text)
            choice_data = ChatCompletionResponseStreamChoice(
                index=0,
                delta=DeltaMessage(content=new_text),
                finish_reason=None
            )
            chunk = ChatCompletionResponse(model=model_name, choices=[choice_data], object="chat.completion.chunk")
            yield "{}".format(chunk.model_dump_json(exclude_unset=True))
            return
        new_response = response.output.text
        if len(new_response) == current_length:
            continue
        new_text = new_response[current_length:]
        current_length = len(new_response)
        choice_data = ChatCompletionResponseStreamChoice(
            index=0,
            delta=DeltaMessage(content=new_text),
            finish_reason=None
        )
        chunk = ChatCompletionResponse(model=model_name, choices=[choice_data], object="chat.completion.chunk")
        yield "{}".format(chunk.model_dump_json(exclude_unset=True))

    choice_data = ChatCompletionResponseStreamChoice(
        index=0,
        delta=DeltaMessage(),
        finish_reason="stop"
    )
    chunk = ChatCompletionResponse(model=model_name, choices=[choice_data], object="chat.completion.chunk")
    yield "{}".format(chunk.model_dump_json(exclude_unset=True))
    yield '[DONE]'
