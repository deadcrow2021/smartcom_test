from celery import Celery
from celery.schedules import crontab

from src.core.settings import redis_settings, rabbit_settings

celery_app = Celery(
    "worker",
    backend=f'redis://{redis_settings.redis_host}:6379/0',
    broker=f'pyamqp://{rabbit_settings.rabbit_user}:{rabbit_settings.rabbit_password}@{rabbit_settings.rabbit_host}:5672/'
)

celery_app.conf.broker_connection_retry_on_startup = True
celery_app.autodiscover_tasks(['src.tasks'])
