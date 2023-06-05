from typing import Any, List, Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status

from .crud import cargo
from .schemas import CargoGet, CargoCreate, CargoInDB, CargoList, CargoUpdate
from src.db.session import get_session


router = APIRouter(prefix="/cargo", tags=["Cargo"])


@router.get("/{cargo_id}", status_code=200, response_model=CargoGet)
def get_cargo(
    *,
    cargo_id: int,
    db_session: Session = Depends(get_session),
) -> Any:
    result = cargo.get(db_session=db_session, id=cargo_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cargo with ID {cargo_id} not found",
        )

    return result


@router.get("/", status_code=200, response_model=List[CargoList])
def list_cargo(
    db_session: Session = Depends(get_session),
    weight: Annotated[int, Query()] = None,
    miles_to_cargo: Annotated[int, Query()] = 450,
) -> List[CargoList]:
    results = cargo.list(
        db_session=db_session, weight=weight, miles_to_cargo=miles_to_cargo
    )
    return results


@router.post("/", status_code=201, response_model=CargoInDB)
def create_cargo(
    *,
    new_cargo: CargoCreate,
    db_session: Session = Depends(get_session),
) -> dict:
    result = cargo.create(db_session=db_session, obj_in=new_cargo)

    return result


@router.patch("/{cargo_id}", status_code=201, response_model=CargoInDB)
def update_cargo(
    *,
    cargo_id: int,
    update_cargo: CargoUpdate,
    db_session: Session = Depends(get_session),
) -> Any:
    result = cargo.update(db_session=db_session, id=cargo_id, obj=update_cargo)
    return result


@router.delete("/{cargo_id}", status_code=204)
def delete_cargo(
    *,
    cargo_id: int,
    db_session: Session = Depends(get_session),
) -> None:
    cargo.delete(db_session=db_session, id=cargo_id)
