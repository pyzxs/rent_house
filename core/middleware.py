# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/12
# @File           : middleware.py
# @desc           : 路由中间件
"""
官方文档——中间件：https://fastapi.tiangolo.com/tutorial/middleware/
官方文档——高级中间件：https://fastapi.tiangolo.com/advanced/middleware/
"""
import time
from fastapi import Request, Response
from starlette.middleware.cors import CORSMiddleware

from config import settings
from core.log import logger
from fastapi import FastAPI


def write_request_log(request: Request, response: Response):
    http_version = f"http/{request.scope['http_version']}"
    content_length = response.raw_headers[0][1].decode("UTF-8")
    process_time = response.headers["X-Process-Time"]
    content = f"http.log_message: '{request.method} {request.url} {http_version}' {response.status_code}" \
              f" {response.charset} {content_length} {process_time}"
    logger.info(content)


def register_request_log_middleware(app: FastAPI):
    """
    记录请求日志中间件
    :param app:
    :return:
    """

    @app.middleware("http")
    async def request_log_middleware(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        write_request_log(request, response)
        return response


def register_jwt_refresh_middleware(app: FastAPI):
    """
    JWT刷新中间件
    :param app:
    :return:
    """

    @app.middleware("http")
    async def jwt_refresh_middleware(request: Request, call_next):
        response = await call_next(request)
        refresh = request.scope.get('if-refresh', 0)
        response.headers["if-refresh"] = str(refresh)
        return response


def http_request_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS
    )