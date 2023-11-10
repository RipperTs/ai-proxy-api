import traceback

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
import logging
import time

from starlette import status
from starlette.responses import JSONResponse

from service.proxy_service import do_proxy


def register_all_handler(app: FastAPI):
    """
    注册全局handler
    :param app:
    :return:
    """
    register_exception(app)
    register_cors(app)
    register_middleware(app)


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
                                      "message": "参数不全或参数错误"}),
        )

    # 捕获全部异常
    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        logging.error(f"全局异常\nURL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"code": 500, "data": {"tip": "系统繁忙,请稍后再试!", "exc": str(exc)}, "message": "fail"},
        )

    # 捕获断言错误，用于返回错误状态
    @app.exception_handler(AssertionError)
    async def asser_exception_handler(request: Request, exc: AssertionError):
        logging.error(f"断言错误，URL：{request.url}, 此处条件不符合")
        logging.info(f"------------------------{exc.args}")
        state = exc.args[0] if exc.args else 0
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"code": 422, "data": {"tip": state}, "message": "fail"}, )


def register_cors(app: FastAPI):
    """
    支持跨域
    :param app:
    :return:
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_middleware(app: FastAPI):
    """
    请求响应拦截
    :param app:
    :return:
    """

    @app.middleware("http")
    async def proxy(request: Request, call_next):
        if request.url.path.startswith("/ai-proxy"):
            return await call_next(request)
        return await do_proxy(request)
