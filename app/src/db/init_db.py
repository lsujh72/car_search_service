import csv
from typing import List

from sqlalchemy.orm import Session

from src.location.schemas import LocationCreate
from src.location.models import Location

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


def init_db(db_session: Session) -> None:
    locations = read_file()
    db_session.bulk_insert_mappings(Location, locations)
    db_session.commit()
