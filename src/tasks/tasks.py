from time import sleep

from tasks.celery_app import celery_instance


@celery_instance.task
def test_task():
    # Run task `celery --app=tasks.celery_app:celery_instance worker -l INFO`
    sleep(5)
    print("я молодец")
