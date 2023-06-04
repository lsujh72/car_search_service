from pydantic import BaseModel, Field

from typing import List


class CargoBase(BaseModel):
    weight: int = Field(ge=1, le=1000)
    description: str


class CargoCreate(CargoBase):
    location_pick_up_zip: int
    location_delivery_zip: int


class CargoUpdate(CargoBase):
    pass


class CargoInDBBase(CargoBase):
    id: int
    location_pick_up_id: int
    location_delivery_id: int

    class Config:
        orm_mode = True


class Cars(BaseModel):
    unique_number: str
    distance: float


class CargoGet(CargoBase):
    location_pick_up: tuple
    location_delivery: tuple
    cars: List[Cars]


class CargoList(CargoBase):
    location_pick_up: tuple
    location_delivery: tuple
    number_nearby_cars: int | None


class CargoInDB(CargoInDBBase):
    pass
