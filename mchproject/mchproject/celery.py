from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mchproject.settings')

app = Celery('mchproject')


app.conf.enable_utc = False
app.conf.update(timzone = 'Asia/Kolkata')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
