import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stratagems.settings')

app = Celery('stratagems')

app.conf.update(timezone='Europe/Moscow')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'parse_data_every_2_hours': {
        'task': 'news.parser.test',
        'schedule': crontab(minute='*/1'),
    }
}