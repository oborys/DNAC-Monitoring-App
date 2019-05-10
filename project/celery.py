#
# Copyright (c) 2019 Cisco Systems
# Licensed under the MIT License
#

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(['app'])

app.conf.beat_schedule = {
    'path_trace_check_every_1_minute': {
        'task': 'app.tasks.path_trace_check',
        'schedule': crontab(minute="*/1"),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },
    'check_name_every_1_minute': {
        'task': 'app.tasks.check_name',
        'schedule': crontab(minute="*/1"),
    },
    'update_service_ticket_every_1_hour': {
        'task': 'app.tasks.update_ticket',
        'schedule': crontab(hour="*/1"),
    },
    'check_config_every_1_minute': {
        'task': 'app.tasks.config_check',
        'schedule': crontab(minute="*/1"),
    },
    'check_reachability_every_1_minute': {
        'task': 'app.tasks.device_reachability',
        'schedule': crontab(minute="*/1"),
    },
    'send_daily_report_every_work_day': {
        'task': 'app.tasks.daily_report',
        'schedule': crontab(day_of_week="mon-fri", hour=9, minute=0)
    }
}
