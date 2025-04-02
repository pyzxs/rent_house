# -*- coding: UTF-8 -*-
# @Project ：rent_house 
# @version : 1.0
# @File    ：setting.py
# @Author  ：ben
# @Date    ：2025/4/2 下午12:33 
# @desc    : setting configuration
import os
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
load_dotenv()

"""
system version
"""
VERSION = "1.0.0"

"""warning: not open on production environment """
DEBUG = False if os.getenv("DEBUG", "false").lower() == "false" else True

"""
import database connection
"""
if DEBUG:
    from config.development import *
else:
    from config.production import *

"""project root path"""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

"""
Whether to enable login authentication
Only applicable to simple interfaces
If the interface is strongly related to authentication, it cannot be used
"""
OAUTH_ENABLE = True
"""
Configure OAuth2 password flow authentication method
Official documentation: https://fastapi.tiangolo.com/tutorial/security/first-steps/#fastapi-oauth2passwordbearer
auto_error:(bool) Optional parameter, default is True. When validation fails, if set to True, FastAPI will automatically return a 401 unauthorized response. If set to False, you need to handle authentication failure yourself.
Here, auto_error is set to False because OpenAuth (open authentication) allows access without authentication.
If set to True, FastAPI will automatically throw an error, which would disable OpenAuth when no authentication is provided, so True cannot be used.
"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login", auto_error=False) if OAUTH_ENABLE else lambda: ""
"""A secure random key that will be used to sign JWT tokens"""
SECRET_KEY = 'vgb0tnl9d58+6n-6h-ea&u^1#s0ccp!794=kbvqacjq75vzps$'
"""Set the signing algorithm for JWT tokens"""
ALGORITHM = "HS256"
"""Expiration time of access_token, one day"""
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
"""Expiration time of refresh_token, used for refreshing tokens, two days"""
REFRESH_TOKEN_EXPIRE_MINUTES = 1440 * 2
"""Cache time of access_token, used for refreshing tokens, 30 minutes"""
ACCESS_TOKEN_CACHE_MINUTES = 1440

"""
Mount the temporary file directory and add route access; this route will not appear in the API documentation
TEMP_DIR: Absolute path of the temporary file directory
Official documentation: https://fastapi.tiangolo.com/tutorial/static-files/
"""
TEMP_DIR = os.path.join(BASE_DIR, "temp")

"""
Mount the static directory and add route access; this route will not appear in the API documentation
STATIC_URL: Route access
STATIC_ROOT: Absolute path of the static file directory
Official documentation: https://fastapi.tiangolo.com/tutorial/static-files/
"""
STATIC_ENABLE = True
STATIC_URL = "/media"
STATIC_DIR = "static"
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_DIR)

"""
Cross-Origin Resource Sharing (CORS) solution
"""
# List of allowed domains, * means all
ALLOW_ORIGINS = ["*"]
# Whether to support carrying cookies
ALLOW_CREDENTIALS = True
# Set allowed HTTP methods for CORS, such as get, post, put, etc.
ALLOW_METHODS = ["*"]
# Allowed headers, which can be used for identification or other purposes.
ALLOW_HEADERS = ["*"]

"""
Other project configurations
"""
DEFAULT_AVATAR = STATIC_URL + "/default/avatar.png"
# Default password, "0" defaults to the last six digits of the phone number
DEFAULT_PASSWORD = "123456"
# Maximum number of incorrect password or verification code attempts during login by default
DEFAULT_AUTH_ERROR_MAX_NUMBER = 5
# Whether to enable saving local logs for each request
REQUEST_LOG_RECORD = False

"""
middleware configuration
"""
MIDDLEWARES = [
    "core.middleware.http_request_cors_middleware",
    "core.middleware.register_request_log_middleware" if REQUEST_LOG_RECORD else None,
    "core.middleware.register_jwt_refresh_middleware"
]

"""
global event configuration
"""
EVENTS = [
    "core.event.connect_redis" if CACHE_DB_ENABLE else None,
]
