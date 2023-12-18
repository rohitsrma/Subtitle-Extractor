from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_processing.settings')
celery_app = Celery('video_processing')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
@celery_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))