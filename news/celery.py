import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')

app = Celery('news')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_valute_rates': {
        'task': 'newscontent.tasks.api_rates',
        'schedule': 15,
    },
    'update_weather': {
        'task': 'newscontent.tasks.api_weather',
        'schedule': 12,
    }
}


# celery -A news worker -B
# celery -A news beat
