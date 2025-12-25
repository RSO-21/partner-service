from sqlalchemy import Column, Integer, String, Boolean, Float
from .db import Base


class Partner(Base):
    __tablename__ = "partners"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    tenant_id = Column(String, nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)