import os
from celery import Celery
import django_celery_results

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
app = Celery('config',)
             # broker='amqp://rabbitmq:rabbitmq@test:5672',)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.result_backend = 'django-db'


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
