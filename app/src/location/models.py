from sqlalchemy import Column, Integer, String, Float

from src.db.base_class import Base


class Location(Base):
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    state_name = Column(String)
    zip = Column(Integer, nullable=False, index=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
