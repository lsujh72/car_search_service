from typing import List, Union, Optional, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.crud.base import CRUDBase, CreateSchemaType, ModelType, UpdateSchemaType
from .schemas import CarCreate, CarUpdate
from .models import Car
from src.location.models import Location
from src.utils.query import SQL_QUERY_RANDOM_LOCATION


class CRUDCar(CRUDBase[Car, CarCreate, CarUpdate]):
    def list(self, db_session: Session) -> List[ModelType]:
        objs: List[ModelType] = db_session.query(self.model).join(Location).all()
        return objs

    def create(self, db_session: Session, obj_in: CreateSchemaType) -> ModelType:
        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = obj_in.dict(exclude_unset=True)

        location = db_session.execute(text(SQL_QUERY_RANDOM_LOCATION)).fetchone()
        obj_in_data.update({'location_current_id': location[0]})

        db_obj = self.model(**obj_in_data)
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def update(self, db_session: Session, id: Any,
               obj: Union[UpdateSchemaType, Dict[str, Any]]) -> Optional[ModelType]:
        db_obj: Optional[ModelType] = db_session.get(self.model, id)
        obj_data = jsonable_encoder(db_obj)
        
        if isinstance(obj, dict):
            update_data = obj
        else:
            update_data = obj.dict(exclude_unset=True)

        zip = update_data.pop('zip')
        location_id = db_session.query(Location).filter_by(zip=zip).first().id
        update_data.update({'location_current_id': location_id})
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj


car = CRUDCar(Car)
