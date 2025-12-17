from celery import Celery
from app.config import settings

celery = Celery(
    "instaboost",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)
celery.conf.task_routes = {"app.worker.tasks.*": {"queue": "default"}}
