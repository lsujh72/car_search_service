from sqlalchemy.orm import Session
from sqlalchemy import text

from src.car.models import Car
from src.location.models import Location
from src.utils.query import SQL_QUERY_RANDOM_LOCATION
from src.db.session import create_session


def update_locations() -> None:
    db_session = create_session()
    try:
        cars = db_session.query(Car).join(Location).all()
        locations = get_locations_ids(db_session, len(cars))
        update_data = []
        for car, location in zip(cars, locations):
            print(car, location)
            update_data.append({"id": car.id, "location_current_id": location[0]})

        db_session.bulk_update_mappings(Car, update_data)
        db_session.commit()
    except Exception:
        db_session.rollback()
    finally:
        db_session.close()


def get_location_id(db_session: Session, zip: int) -> int:
    return db_session.query(Location).filter_by(zip=zip).first().id


def get_locations_ids(db_session: Session, count: int) -> list:
    return db_session.execute(text(SQL_QUERY_RANDOM_LOCATION)).fetchmany(count)
