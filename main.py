# -*- coding: UTF-8 -*-
# @Project ：rent_house 
# @version : 1.0
# @File    ：main.py
# @Author  ：ben
# @Date    ：2025/4/2 下午1:36 
# @desc    : main

"""
FastApi 更新文档：https://github.com/tiangolo/fastapi/releases
FastApi Github：https://github.com/tiangolo/fastapi
Typer 官方文档：https://typer.tiangolo.com/
"""

import typer
import uvicorn
from fastapi.openapi.docs import get_swagger_ui_html

from config import settings,routers
from core.database import engine, Base
from core.event import lifespan
from core.exception import register_exception
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.module import import_modules

from scripts import scheduler, initialize

shell_app = typer.Typer()


def create_app():
    """启动项目"""
    app = FastAPI(
        title="rent_house",
        description="rent house project",
        version=settings.VERSION,
        docs_url=None,
        lifespan=lifespan,
    )

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui():
        return get_swagger_ui_html(
            openapi_url="/openapi.json",  # 指定 OpenAPI 文档路径
            title="rent house",  # 自定义页面标题
            swagger_js_url="/media/swagger-ui/swagger-ui-bundle.js",  # 本地 JS 文件
            swagger_css_url="/media/swagger-ui/swagger-ui.css",  # 本地 CSS 文件
            swagger_favicon_url="/media/swagger-ui/favicon.png"  # 本地 favicon 图标
        )

    Base.metadata.create_all(bind=engine)
    import_modules(settings.MIDDLEWARES, "middleware", app=app)

    # 全局异常捕捉处理
    register_exception(app)

    # 路由
    if settings.STATIC_ENABLE:
        app.mount(settings.STATIC_URL, app=StaticFiles(directory=settings.STATIC_ROOT))

    for url in routers.urlpatterns:
        app.include_router(url["ApiRouter"], prefix=url["prefix"], tags=url["tags"])

    return app


@shell_app.command()
def run(
        host: str = typer.Option(default='0.0.0.0', help='监听主机IP，默认开放给本网络所有主机'),
        port: int = typer.Option(default=8088, help='监听端口')
):
    """
    启动项目

    factory: 在使用 uvicorn.run() 启动 ASGI 应用程序时，可以通过设置 factory 参数来指定应用程序工厂。
    应用程序工厂是一个返回 ASGI 应用程序实例的可调用对象，它可以在启动时动态创建应用程序实例。
    """
    if settings.DEBUG:
        uvicorn.run(app='main:create_app', host=host, port=port, reload=True, factory=True)
    else:
        uvicorn.run(app='main:create_app', host=host, port=port, factory=True,workers=2)


@shell_app.command()
def queue():
    """
    启动服务脚本

    celery --app schedule worker -l info -c 4  -E -P eventlet
    """
    scheduler.queue()


@shell_app.command()
def crontab():
    """
    启动服务脚本

    celery --app schedule beat -l info
    """
    scheduler.crontab()


@shell_app.command()
def migrate():
    """
    生成角色、管理员、菜单信息

    """
    print("initialize database")
    if settings.DEBUG:
        initialize.migrate()
    else:
        print("online can not migrate")


if __name__ == '__main__':
    try:
        shell_app()
    except KeyboardInterrupt:
        print("检测到中断信号，正在优雅地关闭程序...")
    except Exception as e:
        print(f"发生了一个错误: {e}")
    finally:
        print("执行清理工作...")
