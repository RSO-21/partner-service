from pydantic import BaseModel
from typing import Optional


# ─────────────────────────────
# Base schema (shared fields)
# ─────────────────────────────
class PartnerBase(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    active: bool = True
    tenant_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


# ─────────────────────────────
# Create schema
# ─────────────────────────────
class PartnerCreate(PartnerBase):
    name: str
    address: str
    latitude: float
    longitude: float


# ─────────────────────────────
# Update schema (all optional)
# ─────────────────────────────
class PartnerUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    active: Optional[bool] = None
    tenant_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


# ─────────────────────────────
# Read schema (DB → API)
# ─────────────────────────────
class PartnerRead(PartnerBase):
    id: str  # UUID stored as string

    model_config = {
        "from_attributes": True
    }


# ─────────────────────────────
# Nearby search request
# ─────────────────────────────
class PartnerNearbyRequest(BaseModel):
    lat: float
    lng: float
    radius_km: float = 5.0
