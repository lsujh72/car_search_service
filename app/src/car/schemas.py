from pydantic import BaseModel, Field


class CarBase(BaseModel):
    unique_number: str = Field(regex=r"^\d{4}[A-Z]{1}$")
    carrying: int = Field(ge=1, le=1000)


class CarCreate(CarBase):
    location_current_id: int


class CarUpdate(CarBase):
    zip: int | None
    carrying: int | None
    unique_number: str = Field(regex=r"^\d{4}[A-Z]{1}$", default=None)


class CarInDBBase(CarBase):
    id: int
    location_current_id: int

    class Config:
        orm_mode = True


class CarInDB(CarInDBBase):
    pass
