# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/16
# @File           : event.py
# @desc           : 主配置文件
from fastapi import FastAPI

from config import settings
from redis import asyncio as aioredis
from redis.exceptions import AuthenticationError, TimeoutError, RedisError
from contextlib import asynccontextmanager

from core.log import logger
from core.module import import_modules_async


@asynccontextmanager
async def lifespan(app: FastAPI):

    await import_modules_async(settings.EVENTS, "全局事件", app=app, status=True)

    yield

    await import_modules_async(settings.EVENTS, "全局事件", app=app, status=False)


async def connect_redis(app: FastAPI, status: bool):
    """
    把 redis 挂载到 app 对象上面

    博客：https://blog.csdn.net/wgPython/article/details/107668521
    博客：https://www.cnblogs.com/emunshe/p/15761597.html
    官网：https://aioredis.readthedocs.io/en/latest/getting-started/
    Github: https://github.com/aio-libs/aioredis-py

    aioredis.from_url(url, *, encoding=None, parser=None, decode_responses=False, db=None, password=None, ssl=None,
    connection_cls=None, loop=None, **kwargs) 方法是 aioredis 库中用于从 Redis 连接 URL 创建 Redis 连接对象的方法。

    以下是该方法的参数说明：
    url：Redis 连接 URL。例如 redis://localhost:6379/0。
    encoding：可选参数，Redis 编码格式。默认为 utf-8。
    parser：可选参数，Redis 数据解析器。默认为 None，表示使用默认解析器。
    decode_responses：可选参数，是否将 Redis 响应解码为 Python 字符串。默认为 False。
    db：可选参数，Redis 数据库编号。默认为 None。
    password：可选参数，Redis 认证密码。默认为 None，表示无需认证。
    ssl：可选参数，是否使用 SSL/TLS 加密连接。默认为 None。
    connection_cls：可选参数，Redis 连接类。默认为 None，表示使用默认连接类。
    loop：可选参数，用于创建连接对象的事件循环。默认为 None，表示使用默认事件循环。
    **kwargs：可选参数，其他连接参数，用于传递给 Redis 连接类的构造函数。

    aioredis.from_url() 方法的主要作用是将 Redis 连接 URL 转换为 Redis 连接对象。
    除了 URL 参数外，其他参数用于指定 Redis 连接的各种选项，例如 Redis 数据库编号、密码、SSL/TLS 加密等等。可以根据需要选择使用这些选项。

    health_check_interval 是 aioredis.from_url() 方法中的一个可选参数，用于设置 Redis 连接的健康检查间隔时间。
    健康检查是指在 Redis 连接池中使用的连接对象会定期向 Redis 服务器发送 PING 命令来检查连接是否仍然有效。
    该参数的默认值是 0，表示不进行健康检查。如果需要启用健康检查，则可以将该参数设置为一个正整数，表示检查间隔的秒数。
    例如，如果需要每隔 5 秒对 Redis 连接进行一次健康检查，则可以将 health_check_interval 设置为 5
    :param app:
    :param status:
    :return:
    """
    if status:
        rd = aioredis.from_url(settings.CACHE_DB_URL, decode_responses=True, health_check_interval=1)
        app.state.redis = rd
        try:
            response = await rd.ping()
            if response:
                logger.info("Redis connect success!")
            else:
                logger.info("Redis connect failed")
        except AuthenticationError as e:
            raise AuthenticationError(f"Redis 连接认证失败，用户名或密码错误: {e}")
        except TimeoutError as e:
            raise TimeoutError(f"Redis 连接超时，地址或者端口错误: {e}")
        except RedisError as e:
            raise RedisError(f"Redis 连接失败: {e}")
    else:
        logger.info("Redis connect closed")
        await app.state.redis.close()

