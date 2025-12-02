from sqlalchemy import Column, Integer, String, Boolean
from .db import Base


class Partner(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    tenant_id = Column(String, nullable=True)