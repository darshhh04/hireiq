from celery import Celery
from app.config import settings

celery = Celery("hireiq", broker=settings.redis_url, backend=settings.redis_url)

@celery.task
def ping():
    return "pong"