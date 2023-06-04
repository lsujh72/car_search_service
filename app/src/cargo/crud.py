from typing import List, Any, Optional

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.crud.base import CRUDBase, ModelType, CreateSchemaType
from src.utils.geo import number_of_nearby_cars, cars_distance
from src.utils.query import SQL_QUERY
from utils.location import get_location_id
from .schemas import CargoCreate, CargoUpdate, CargoList, CargoGet
from .models import Cargo


class CRUDCargo(CRUDBase[Cargo, CargoCreate, CargoUpdate]):
    def create(self, db_session: Session, obj_in: CreateSchemaType) -> ModelType:
        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = obj_in.dict(exclude_unset=True)

        location_id = get_location_id(
            db_session, obj_in_data.pop("location_pick_up_zip")
        )
        obj_in_data.update({"location_pick_up_id": location_id})

        location_id = get_location_id(
            db_session, obj_in_data.pop("location_delivery_zip")
        )
        obj_in_data.update({"location_delivery_id": location_id})

        db_obj = self.model(**obj_in_data)
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def list(
        self, db_session: Session, weight: int, miles_to_cargo: int
    ) -> List[CargoList]:
        params = {}
        sql_query = SQL_QUERY
        if weight:
            sql_query += " WHERE ca.weight = :weight"
            params.update({"weight": weight})
        results = db_session.execute(text(sql_query), params)
        objs = [row._mapping for row in results]
        results = []
        for obj in objs:
            location_pick_up = (obj.lat_1, obj.lng_1)
            location_delivery = (obj.lat_2, obj.lng_2)
            number_nearby_cars = number_of_nearby_cars(
                db_session, location_pick_up, miles_to_cargo
            )
            results.append(
                CargoList(
                    description=obj.description,
                    weight=obj.weight,
                    location_pick_up=location_pick_up,
                    location_delivery=location_delivery,
                    number_nearby_cars=number_nearby_cars,
                ).dict()
            )

        return results

    def get(self, db_session: Session, id: Any) -> Optional[ModelType]:
        sql_query = f"{SQL_QUERY} WHERE ca.id=:id;"
        obj = db_session.execute(text(sql_query), params={"id": id}).fetchone()._mapping

        location_pick_up = (obj.lat_1, obj.lng_1)

        cars = cars_distance(
            db_session,
            location_pick_up,
        )
        result = CargoGet(
            cars=cars,
            description=obj.description,
            weight=obj.weight,
            location_pick_up=(obj.lat_1, obj.lng_1),
            location_delivery=(obj.lat_2, obj.lng_2),
        )
        if result is None:
            raise HTTPException(status_code=404, detail="Not Found")
        return result


cargo = CRUDCargo(Cargo)
