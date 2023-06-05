from typing import Any, Generic, List, Optional, Type, TypeVar, Union, Dict

import sqlalchemy
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from src.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db_session: Session, id: Any) -> Optional[ModelType]:
        obj: Optional[ModelType] = db_session.get(self.model, id)
        if obj is None:
            raise HTTPException(status_code=404, detail="Not Found")
        return obj

    def list(self, db_session: Session, *args, **kwargs) -> List[ModelType]:
        objs: List[ModelType] = db_session.query(self.model).all()
        return objs

    def create(self, db_session: Session, obj_in: CreateSchemaType) -> ModelType:
        db_obj: ModelType = self.model(**obj_in.dict())
        db_session.add(db_obj)
        try:
            db_session.commit()
        except sqlalchemy.ext.IntegrityError as e:
            db_session.rollback()
            if "duplicate key" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Conflict Error"
                )
            else:
                raise e
        return db_obj

    def update(
        self, db_session: Session, id: Any, obj: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> Optional[ModelType]:
        db_obj: Optional[ModelType] = db_session.get(self.model, id)
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj, dict):
            update_data = obj
        else:
            update_data = obj.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def delete(self, db_session: Session, id: Any) -> None:
        db_obj = db_session.get(self.model, id)
        db_session.delete(db_obj)
        db_session.commit()
