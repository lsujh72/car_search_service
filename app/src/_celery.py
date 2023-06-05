from celery import Celery
from celery.schedules import crontab

from src.config import CELERY_BROKER_URL


celery_app = Celery("tasks")
celery_app.conf.broker_url = CELERY_BROKER_URL


celery_app.conf.beat_schedule = {
    "update_every_3_min": {
        "task": "celery_app.tasks.car_update_locations",
        "schedule": crontab(minute="*/3"),
    }
}

celery_app.conf.timezone = "UTC"
celery_app.conf.update(task_track_started=True)
celery_app.autodiscover_tasks()


@celery_app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
