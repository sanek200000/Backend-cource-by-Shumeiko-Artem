from celery import Celery

from conf import settings


celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "tasks.tasks",
    ],
)
