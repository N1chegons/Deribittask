from celery import Celery

from src.config import settings

celery_app = Celery(
    'crypto_tasks',
    backend=settings.REDIS_URL,
    include=["src.utilits"]
)

celery_app.conf.broker_url = settings.REDIS_URL

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    worker_pool='gevent',

    beat_schedule={
        'fetch-prices-every-minute': {
            'task': 'fetch_prices_task',
            'schedule': 60.0,
        },
    },
    beat_scheduler='celery.beat:PersistentScheduler',
)

celery_app.autodiscover_tasks()