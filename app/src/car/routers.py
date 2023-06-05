from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .crud import car
from .schemas import CarInDB, CarBase, CarUpdate
from src.db.session import get_session


router = APIRouter(prefix="/cars", tags=["Cars"])


@router.post("/", status_code=201, response_model=CarInDB)
def create_car(
    *,
    new_car: CarBase,
    db_session: Session = Depends(get_session),
) -> dict:
    result = car.create(db_session=db_session, obj_in=new_car)

    return result


@router.patch("/{car_id}", status_code=201, response_model=CarInDB)
def update_car(
    *,
    car_id: int,
    update_car: CarUpdate,
    db_session: Session = Depends(get_session),
) -> Any:
    result = car.update(db_session=db_session, id=car_id, obj=update_car)
    return result
