from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.car.models import Car
from src.cargo.models import Cargo
from src.db.base_class import Base
from src.location.models import Location
from src.app import create_app
from src.db.session import get_session

SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/test_db"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def app_client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app = create_app()
    app.dependency_overrides[get_session] = override_get_db

    yield TestClient(app)


@pytest.fixture()
def create_location(db: scoped_session) -> Generator[Location, None, None]:
    location = Location(
        city="Adjuntas",
        state_name="Puerto Rico",
        zip=601,
        lat=18.180269241333008,
        lng=-66.7526626586914,
    )
    db.add(location)
    db.commit()
    yield location


@pytest.fixture()
def create_location_1(db: scoped_session) -> Generator[Location, None, None]:
    location = Location(
        city="Maunabo",
        state_name="Puerto Rico",
        zip=707,
        lat=18.017520904541016,
        lng=-65.92127227783203,
    )
    db.add(location)
    db.commit()
    yield location


@pytest.fixture()
def create_location_2(db: scoped_session) -> Generator[Location, None, None]:
    location = Location(
        city="San Juan",
        state_name="Puerto Rico",
        zip=906,
        lat=18.464460372924805,
        lng=-66.0949935913086,
    )
    db.add(location)
    db.commit()
    yield location


@pytest.fixture()
def create_cargo(
    db: scoped_session, create_location_1: Location, create_location_2: Location
) -> Generator[Cargo, None, None]:
    cargo = Cargo(
        location_pick_up_id=create_location_1.id,
        location_delivery_id=create_location_2.id,
        weight=666,
        description="Delivery",
    )
    db.add(cargo)
    db.commit()
    yield cargo


@pytest.fixture()
def create_car(
    db: scoped_session, create_location: Location
) -> Generator[Car, None, None]:
    car = Car(
        location_current_id=create_location.id,
        carrying=1000,
        unique_number="1359K",
    )
    db.add(car)
    db.commit()
    yield car
