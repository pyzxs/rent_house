# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/12
# @File           : logger.py
# @desc           : 日志文件

import os
import time
from logging import Logger
import logging
from logging.handlers import RotatingFileHandler

from config.settings import BASE_DIR,LOG_FILENAME,LOG_FILE_MAX_SIZE,LOG_FILE_BACKUP_COUNT,LOG_LEVEL,LOG_FORMAT,LOG_RECORDER


# 日志记录器
logger = logging.getLogger(LOG_RECORDER)
logger.setLevel(LOG_LEVEL)
log_filename = BASE_DIR + LOG_FILENAME
log_handler = RotatingFileHandler(log_filename, maxBytes=LOG_FILE_MAX_SIZE, backupCount=LOG_FILE_BACKUP_COUNT, encoding='utf-8')
log_formatter = logging.Formatter(LOG_FORMAT)
log_handler.setFormatter(log_formatter)

logger.addHandler(log_handler)
