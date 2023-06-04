from src._celery import celery_app


@celery_app.task(bind=True)
def car_update_locations():
    from src.utils.location import update_locations
    from src.db.session import SessionLocal
    with SessionLocal() as session:
        update_locations(session)
    return True
