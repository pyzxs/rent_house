# -*- coding: UTF-8 -*-
# @Project ：rent_house 
# @version : 1.0
# @File    ：main.py
# @Author  ：ben
# @Date    ：2025/4/2 13:36 
# @desc    : main entry point

"""
FastApi releases: https://github.com/tiangolo/fastapi/releases
FastApi Github: https://github.com/tiangolo/fastapi
Typer documentation: https://typer.tiangolo.com/
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
    """Initialize and start the project"""
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
            openapi_url="/openapi.json",  # OpenAPI document path
            title="rent house",  # Custom page title
            swagger_js_url="/media/swagger-ui/swagger-ui-bundle.js",  # Local JS file
            swagger_css_url="/media/swagger-ui/swagger-ui.css",  # Local CSS file
            swagger_favicon_url="/media/swagger-ui/favicon.png"  # Local favicon
        )

    Base.metadata.create_all(bind=engine)
    import_modules(settings.MIDDLEWARES, "middleware", app=app)

    # Global exception handling
    register_exception(app)

    # Routers
    if settings.STATIC_ENABLE:
        app.mount(settings.STATIC_URL, app=StaticFiles(directory=settings.STATIC_ROOT))

    for url in routers.urlpatterns:
        app.include_router(url["ApiRouter"], prefix=url["prefix"], tags=url["tags"])

    return app

@shell_app.command()
def run(
        host: str = typer.Option(default='0.0.0.0', help='Host IP to listen on, defaults to all hosts on the network'),
        port: int = typer.Option(default=8000, help='Port to listen on')
):
    """
    Start the project
    
    factory: When using uvicorn.run() to start an ASGI application, the factory parameter can be used to specify an application factory.
    An application factory is a callable that returns an ASGI application instance, allowing dynamic creation of the application instance at startup.
    """
    if settings.DEBUG:
        uvicorn.run(app='main:create_app', host=host, port=port, reload=True, factory=True)
    else:
        uvicorn.run(app='main:create_app', host=host, port=port, factory=True,workers=2)


@shell_app.command()
def queue():
    """
    Start service script
    
    celery --app schedule worker -l info -c 4  -E -P eventlet
    """
    scheduler.queue()

@shell_app.command()
def crontab():
    """
    Start service script
    
    celery --app schedule beat -l info
    """
    scheduler.crontab()

@shell_app.command()
def migrate():
    """
    Generate roles, admin, and menu information
    """
    print("initialize database")
    if settings.DEBUG:
        initialize.migrate()
    else:
        print("Migration not allowed in production environment")

if __name__ == '__main__':
    try:
        shell_app()
    except KeyboardInterrupt:
        print("Interrupt signal detected, shutting down gracefully...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Performing cleanup...")
