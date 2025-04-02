# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/12
# @File           : database.py
# @desc           : Database MySQL connection
from typing import AsyncGenerator, Generator

from redis import Redis
from sqlalchemy import create_engine, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker, Session
from starlette.requests import Request

from config import settings
# Official documentation: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine

# database_url format: dialect+driver://username:password@host:port/database

# echo: If True, the Engine will log all statements as well as their parameter lists to the default log handler, which defaults to sys.stdout.
# If set to "debug", result rows will also be printed to standard output.

# echo_pool: If True, the connection pool will log informational output such as when connections are invalidated as well as when connections are recycled to the default log handler.

# pool_pre_ping: If True, enables the connection pool "pre-ping" feature that tests connections for liveness upon each checkout.

# pool_recycle: This setting causes the pool to recycle connections after the given number of seconds. Default is -1, meaning no timeout.

# pool_size: The number of connections to keep open inside the connection pool.

# pool_timeout: Number of seconds to wait before giving up on getting a connection from the pool.

# max_overflow: The number of connections to allow in connection pool overflow.

from config.settings import SQLALCHEMY_DATABASE_URL, ASYNC_SQLALCHEMY_DATABASE_URL
from core.exception import CustomException

# 创建数据库连接
async_engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URL,
    echo=False,
    echo_pool=False,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=5,
    max_overflow=5,
    connect_args={}
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, echo=False
)

session_local = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)

# 创建数据库会话
session_factory = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    expire_on_commit=True,
    class_=AsyncSession
)


class Base(AsyncAttrs, DeclarativeBase):
    """
    Base mapping class
    This class will be inherited to create each ORM model
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Convert table name to lowercase
        Use custom table name if provided, otherwise use lowercase class name
        """
        table_name = cls.__tablename__
        if not table_name:
            model_name = cls.__name__
            ls = []
            for index, char in enumerate(model_name):
                if char.isupper() and index != 0:
                    ls.append("_")
                ls.append(char)
            table_name = "".join(ls).lower()

        return table_name

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get main database session
    
    Database dependency that will be used for a single request and then closed after the request is finished.
    """
    async with session_factory() as session:
        async with session.begin():
            yield session

def get_db() -> Session:
    """
    Get main database session
    
    Database dependency that will be used for a single request and then closed after the request is finished.
    """
    with session_local() as session:
        yield session

def get_cache(request: Request) -> Redis:
    """
    Get Redis database object
    
    Globally mounted, using a single database object
    """
    if not settings.CACHE_DB_ENABLE:
        raise CustomException("Please configure Redis database connection and enable it first!", desc="Please enable application/settings.py: CACHE_DB_ENABLE")
    return request.app.state.redis
