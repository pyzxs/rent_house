# -*- coding: UTF-8 -*-
# @Project ：rent_house 
# @version : 1.0
# @File    ：production.py
# @Author  ：ben
# @Date    ：2025/4/2 下午12:35 
# @desc    : production online environment

"""
MySQL database configuration
Official documentation for connection engine: https://www.osgeo.cn/sqlalchemy/core/engines.html
Database connection format: mysql+asyncmy://username:password@host:port/database_name
"""
ASYNC_SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://root:123456@127.0.0.1:3306/rent_house?charset=utf8mb4"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@127.0.0.1:3306/rent_house?charset=utf8mb4"

"""
Using Redis as cache
Format: "redis://:password@host:port/database_name"
"""

CACHE_DB_ENABLE = True
CACHE_DB_URL = "redis://:123456@127.0.0.1:6379/0"
CACHE_EXPIRE = 60 * 60 * 24 * 7

"""
Log configuration
"""
LOG_RECORDER = 'rent_house'
# Set the maximum size of the log file to 10MB (10 * 1024 * 1024 bytes)
LOG_FILE_MAX_SIZE = 10 * 1024 * 1024  # 10MB
# Set the number of log files to keep
LOG_FILE_BACKUP_COUNT = 10  # Keep 10 backup log files
# Log output file path
LOG_FILENAME = "/logs/rent_house.log"  # Path to the log file
# Log level: DEBUG level
LOG_LEVEL = 10
LOG_FORMAT = '%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"'

"""
Message queue and scheduled task processing, requires the following packages:
Redis URL: https://github.com/redis/redis-py
Celery: https://docs.celeryq.dev/

Installation method:
pip install redis
pip install celery
pip install eventlet
"""
SCHEDULE_ENABLE = True
SCHEDULE_BROKER_URL = 'redis://:123456@127.0.0.1:6379/0'
SCHEDULE_RESULT_URL = 'redis://:123456@127.0.0.1:6379/1'
SCHEDULE_RESULT_EXPIRE = 60 * 60 * 24
