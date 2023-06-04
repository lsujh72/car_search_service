from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .crud import car
from .schemas import CarInDB, CarBase, CarUpdate
from src.db.session import get_db


router = APIRouter(prefix="/cars", tags=["Cars"])


@router.post("/", status_code=201, response_model=CarInDB)
def create_car(
    *,
    new_car: CarBase,
    db_session: Session = Depends(get_db),
) -> dict:
    result = car.create(db_session=db_session, obj_in=new_car)

    return result


@router.put("/{car_id}", status_code=201, response_model=CarInDB)
def update_cargo(
    *,
    cargo_id: int,
    update_car: CarUpdate,
    db_session: Session = Depends(get_db),
) -> Any:
    result = car.update(db_session=db_session, id=cargo_id, obj=update_car)
    return result
