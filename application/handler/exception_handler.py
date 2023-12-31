import traceback

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
import logging

from starlette import status
from starlette.responses import JSONResponse

from application.service.lingshi_qwen_service import do_lingshi_qwen_proxy
from application.service.proxy_service import do_openai_proxy
from application.service.users_sercice import get_current_user
import time


def register_exception(app: FastAPI):
    """
    全局异常捕获
    :param app:
    :return:
    """

    # 捕获参数 验证错误
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        捕获请求参数 验证错误
        :param request:
        :param exc:
        :return:
        """
        logging.error(f"参数错误\nURL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder({"code": 10002, "data": {"tip": exc.errors()}, "body": exc.body,
                                      "msg": "参数不全或参数错误"}),
        )

    # 捕获全部异常
    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        if isinstance(exc, HTTPException):
            logging.error(f"HTTP异常\nURL:{request.url}\nHeaders:{request.headers}\nMsg:{str(exc.detail)}\n")
            return JSONResponse(
                status_code=exc.status_code,
                content={"code": exc.status_code, "data": None, "msg": str(exc.detail)},
            )
        logging.error(f"全局异常\nURL:{request.url}\nHeaders:{request.headers}\nMsg:{str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"code": 500, "data": None, "msg": str(exc)},
        )

    # 捕获断言错误，用于返回错误状态
    @app.exception_handler(AssertionError)
    async def asser_exception_handler(request: Request, exc: AssertionError):
        logging.error(f"断言错误，URL：{request.url}, 此处条件不符合")
        logging.info(f"------------------------{exc.args}")
        state = exc.args[0] if exc.args else 0
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"code": 422, "data": None, "msg": state}, )


def register_middleware(app: FastAPI):
    """
    请求响应拦截
    :param app:
    :return:
    """

    @app.middleware("http")
    async def proxy(request: Request, call_next):
        headers = dict(request.headers)
        if request.url.path.startswith("/ai-proxy"):
            if request.url.path in ['/ai-proxy/api/v1/user/login-user', '/ai-proxy/api/v1/user/register-user']:
                return await call_next(request)

            if 'ai-proxy-token' not in headers:
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                    content={"code": 401, "data": None, "msg": "token不存在"})
            token = headers.get('ai-proxy-token', '')
            user_info = await get_current_user(token)
            request.state.user_info = user_info
            return await call_next(request)

        # 处理请求参数
        if "application/json" in headers.get('content-type', 'application/x-www-form-urlencoded'):
            request_data = await request.json()
        else:
            request_data = await request.form()
            request_data = dict(request_data)

        request.state.request_data = request_data
        model_name = request_data.get('model', '')
        if model_name == "qwen-14b-chat" or model_name == "qwen-plus" or model_name == "qwen-7b-chat" or model_name == "qwen-turbo":
            return await do_lingshi_qwen_proxy(request)

        return await do_openai_proxy(request)

