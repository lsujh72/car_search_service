from src._celery import celery_app


@celery_app.task(bind=True)
def car_update_locations():
    from src.utils.location import update_locations

    update_locations()
    return True
