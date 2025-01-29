from celery import Celery

from conf import settings


celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "tasks.tasks",
    ],
)

celery_instance.conf.beat_schedule = {
    "luboe_nazvanie": {
        "task": "booking_today_checkin",
        "schedule": 5,
    }
}
