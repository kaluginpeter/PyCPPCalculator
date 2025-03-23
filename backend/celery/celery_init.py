from celery import Celery

from backend.core.config import settings


app = Celery(
    settings.CELERY_NAME,
    broker=settings.REDIS_BROKER_URL,
    backend=settings.REDIS_BACKEND_URL,
)

app.conf.update(
    result_expires=3600,
)