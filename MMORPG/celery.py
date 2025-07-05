import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MMORPG.settings')

app = Celery('MMORPG')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_mail_with_ad_8pm_sunday': {
        'task': 'ad.tasks.send_out_weekly',
        'schedule': crontab(minute=0, hour=20, day_of_week='sunday'),
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')