# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/15
# @File           : settings.py
# @desc           : 消息队列配置
from celery.schedules import crontab

from config import settings

# Broker，中间件，进行消息传输，使用Redis
broker_url = settings.SCHEDULE_BROKER_URL
# Backend，结果后端，使用Redis
result_backend = settings.SCHEDULE_RESULT_URL
# 任务过期时间
result_expires = settings.SCHEDULE_RESULT_EXPIRE
# 时区配置
timezone = 'Asia/Shanghai'
# 是否在启动期间重试代理连接
broker_connection_retry_on_startup = True
# 任务内容序列
task_serializer = 'json'
# 结果序列化方案
result_serializer = 'json'

accept_content = ['json', 'msgpack']

imports = (  # 导入的任务模块
    'schedule.tasks'
)

# 定时任务配置信息
beat_schedule = {
    'test_task_run': {
        'task': 'schedules.tasks.test_task_run',
        # every 5 minutes
        'schedule': crontab(minute='*/5'),
        'args': ()
    }
}
