from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from math import cos, radians

from ..db import get_db_session
from .. import models, schemas
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ─────────────────────────────
# Router configuration
# ─────────────────────────────
router = APIRouter(
    prefix="/partners",
    tags=["partners"],
)


# ─────────────────────────────
# Tenant handling
# ─────────────────────────────
def get_tenant_id(x_tenant_id: Optional[str] = Header(None)) -> str:
    """
    Extract tenant ID from request header.
    Falls back to 'public' schema if header is missing.
    """
    return x_tenant_id or "public"


def get_db_with_schema(tenant_id: str = Depends(get_tenant_id)):
    """
    Dependency that provides a SQLAlchemy session
    bound to the tenant-specific schema.
    """
    return get_db_session(schema=tenant_id)


# ─────────────────────────────
# List all partners (tenant scoped)
# ─────────────────────────────
@router.get("/", response_model=List[schemas.PartnerRead])
def list_partners(db: Session = Depends(get_db_with_schema)):
    """
    Return all partners for the current tenant.
    """
    return db.query(models.Partner).all()


# ─────────────────────────────
# Nearby partners (approximate geo search)
# ─────────────────────────────
@router.get("/nearby", response_model=List[schemas.PartnerRead])
def get_partners_nearby(
    lat: float,
    lng: float,
    radius_km: float = 5.0,
    db: Session = Depends(get_db_with_schema),
):
    """
    Fetch partners within an approximate radius (km)
    using a bounding-box approach.
    """

    # Convert radius (km) to degree deltas
    lat_delta = radius_km / 111
    lng_delta = radius_km / (111 * cos(radians(lat)))

    partners = (
        db.query(models.Partner)
        .filter(models.Partner.latitude.between(lat - lat_delta, lat + lat_delta))
        .filter(models.Partner.longitude.between(lng - lng_delta, lng + lng_delta))
        .all()
    )

    return partners


# ─────────────────────────────
# Create a new partner
# ─────────────────────────────
@router.post("/", response_model=schemas.PartnerRead, status_code=201)
def create_partner(
    partner: schemas.PartnerCreate,
    db: Session = Depends(get_db_with_schema),
):
    """
    Create a new partner.
    Address and coordinates are required.
    """
    db_partner = models.Partner(**partner.dict())
    db.add(db_partner)
    db.commit()
    db.refresh(db_partner)
    return db_partner


# ─────────────────────────────
# Get a single partner by ID
# ─────────────────────────────
@router.get("/{partner_id}", response_model=schemas.PartnerRead)
def get_partner(partner_id: str, db: Session = Depends(get_db_with_schema)):
    """
    Fetch a partner by ID.
    """
    partner = db.query(models.Partner).filter(models.Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return partner


# ─────────────────────────────
# Update partner (partial update)
# ─────────────────────────────
@router.put("/{partner_id}", response_model=schemas.PartnerRead)
def update_partner(
    partner_id: str,
    partner_update: schemas.PartnerUpdate,
    db: Session = Depends(get_db_with_schema),
):
    """
    Update an existing partner.
    Only fields provided in the request are updated.
    """
    partner = db.query(models.Partner).filter(models.Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    update_data = partner_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(partner, key, value)

    db.commit()
    db.refresh(partner)
    return partner


# ─────────────────────────────
# Delete partner
# ─────────────────────────────
@router.delete("/{partner_id}", status_code=204)
def delete_partner(partner_id: str, db: Session = Depends(get_db_with_schema)):
    """
    Permanently delete a partner.
    """
    partner = db.query(models.Partner).filter(models.Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    db.delete(partner)
    db.commit()
    return None
