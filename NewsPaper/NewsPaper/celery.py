import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    # Executes every Monday morning at 8:00
    'add-weekly-mailings': {
        'task': 'news.tasks.weekly_notify',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
    # Executes every Day, every 6 hours
    'parsing-for-add-news': {
        'task': 'news.tasks.daily_parsing',
        'schedule': crontab(hour='*/6', minute=0)
    }
}

app.autodiscover_tasks()
