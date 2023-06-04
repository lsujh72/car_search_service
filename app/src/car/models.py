from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.db.base_class import Base


class Car(Base):

    id = Column(Integer, primary_key=True, index=True)
    unique_number = Column(String, nullable=False, unique=True)
    location_current_id = Column(Integer, ForeignKey("location.id"))
    location_current = relationship("Location", foreign_keys=[location_current_id])
    carrying = Column(Integer)
