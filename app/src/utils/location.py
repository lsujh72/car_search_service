from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import text

from src.car.models import Car
from src.location.models import Location
from .query import SQL_QUERY_RANDOM_LOCATION


def update_locations(db_session: Session) -> None:
    cars = db_session.query(Car).join(Location).all()
    locations = db_session.execute(text(SQL_QUERY_RANDOM_LOCATION)).fetchmany(len(cars))
    update_data = []
    for car, location in zip(cars, locations):
        update_data.append({"id": car.id, "location_current_id": location[0]})

    db_session.bulk_update_mappings(Car, update_data)
    db_session.commit()


def get_location_id(db_session: Session, zip: int) -> int:
    return db_session.query(Location).filter_by(zip=zip).first().id
