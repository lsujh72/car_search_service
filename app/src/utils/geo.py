from geopy import distance
from sqlalchemy.orm import Session

from src.car import crud


def location_cars(db_session: Session) -> list:
    cars = crud.car.list(db_session=db_session)
    return [
        ((car.location_current.lat, car.location_current.lng), car.unique_number)
        for car in cars
    ]


def count_distance(start: tuple, finish: tuple) -> int:
    return round(distance.distance(start, finish).miles)


def number_of_nearby_cars(
    db_session: Session, location_pick_up: tuple, miles_to_cargo: int = 450
) -> int:
    locations = location_cars(db_session)
    count = 0
    for location_car in locations:
        if count_distance(location_pick_up, location_car[0]) <= miles_to_cargo:
            count += 1
    return count


def cars_distance(db_session: Session, location_pick_up: tuple) -> list:
    locations = location_cars(db_session)
    cars = []
    for location_car in locations:
        _distance = count_distance(location_pick_up, location_car[0])
        unique_number = location_car[1]
        cars.append({"unique_number": unique_number, "distance": _distance})

    return cars
