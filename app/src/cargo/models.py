from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.db.base_class import Base


class Cargo(Base):
    id = Column(Integer, primary_key=True, index=True)
    location_pick_up_id = Column(Integer, ForeignKey("location.id"))
    location_pick_up = relationship("Location", foreign_keys=[location_pick_up_id])

    location_delivery_id = Column(Integer, ForeignKey("location.id"))
    location_delivery = relationship("Location", foreign_keys=[location_delivery_id])

    weight = Column(Integer, nullable=False)
    description = Column(String)
