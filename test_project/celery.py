import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')

app = Celery('logging_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'get_data_and_save_api_on_a_schedule': {
        'task': 'logging_app.tasks.parsing_logs',
        'schedule': crontab(),
    },
}