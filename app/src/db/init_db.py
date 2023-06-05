import csv
import random
from typing import List

from sqlalchemy.orm import Session

from car.schemas import CarCreate
from src.car.models import Car
from src.location.schemas import LocationCreate
from src.location.models import Location
from src.utils.location import get_locations_ids
from src.utils.utils import create_unique_number

file = "./uszips.csv"


def read_file() -> List[LocationCreate]:
    with open(file, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        locations = []
        for row in reader:
            location = LocationCreate(
                zip=row["zip"],
                lat=row["lat"],
                lng=row["lng"],
                state_name=row["state_name"],
                city=row["city"],
            )
            locations.append(location)
        return locations


def create_cars(db_session: Session):
    locations = get_locations_ids(db_session, 20)
    cars = []

    for location in locations:
        car = CarCreate(
            unique_number=create_unique_number(),
            carrying=random.randint(1, 1000),
            location_current_id=location[0],
        )
        cars.append(car)

    db_session.bulk_insert_mappings(Car, cars)
    db_session.commit()


def init_db(db_session: Session) -> None:
    locations = read_file()
    db_session.bulk_insert_mappings(Location, locations)
    db_session.commit()
    create_cars(db_session)
