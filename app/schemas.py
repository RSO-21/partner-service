from pydantic import BaseModel
from typing import Optional


class PartnerBase(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    active: bool = True
    tenant_id: Optional[str] = None


class PartnerCreate(PartnerBase):
    pass


class PartnerUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    active: Optional[bool] = None
    tenant_id: Optional[str] = None


class PartnerRead(PartnerBase):
    id: int

    model_config = {
        "from_attributes": True
    }
