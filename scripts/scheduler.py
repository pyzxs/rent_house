# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/15
# @File           : initialize.py
# @desc           : 主配置文件
import os
import subprocess

from config.settings import BASE_DIR, SCHEDULE_LOG_FILE

log_file = os.path.join(BASE_DIR, SCHEDULE_LOG_FILE)


def queue():
    # start run message queue worker
    queue_args = ['celery', '--app', 'schedule', 'worker', '-l', 'INFO', '-E', '-P', 'eventlet',
                  '-f', log_file]
    subprocess.check_call(queue_args, cwd=BASE_DIR)


def crontab():
    # start run message queue crontab
    cron_args = ['celery', '--app', 'schedule', 'beat', "-l", "INFO", '-f', log_file]
    subprocess.check_call(cron_args, cwd=BASE_DIR)
