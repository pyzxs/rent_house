# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/15
# @File           : __init__.py.py
# @desc           : 主配置文件
import logging
from logging.handlers import RotatingFileHandler

from celery import Celery

app = Celery('schedule')

# 加载配置文件
app.config_from_object('schedule.settings')
