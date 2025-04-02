# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/15
# @File           : settings.py
# @desc           : Message queue configuration
from celery.schedules import crontab
from config import settings

# Broker, middleware for message transmission, using Redis
broker_url = settings.SCHEDULE_BROKER_URL
# Backend, result backend, using Redis
result_backend = settings.SCHEDULE_RESULT_URL
# Task expiration time
result_expires = settings.SCHEDULE_RESULT_EXPIRE
# Timezone configuration
timezone = 'Asia/Shanghai'
# Whether to retry broker connection during startup
broker_connection_retry_on_startup = True
# Task content serialization
task_serializer = 'json'
# Result serialization scheme
result_serializer = 'json'

accept_content = ['json', 'msgpack']

imports = (  # Imported task modules
    'schedule.tasks'
)

# Scheduled task configuration
beat_schedule = {
    'test_task_run': {
        'task': 'schedules.tasks.test_task_run',
        # every 5 minutes
        'schedule': crontab(minute='*/5'),
        'args': ()
    }
}
