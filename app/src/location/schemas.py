from pydantic import BaseModel


class LocationBase(BaseModel):
    city: str
    state_name: str
    zip: int
    lat: float
    lng: float


class LocationCreate(LocationBase):
    pass
