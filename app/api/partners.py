from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from ..db import get_db, get_db_session
from .. import models, schemas

router = APIRouter(
    prefix="/partners",
    tags=["partners"],
)

def get_tenant_id(x_tenant_id: Optional[str] = Header(None)) -> str:
    """Extract tenant ID from header, default to public"""
    return x_tenant_id or "public"

def get_db_with_schema(tenant_id: str = Depends(get_tenant_id)):
    """Dependency to inject DB session with dynamic schema from X-Tenant-ID header"""
    return get_db_session(schema=tenant_id)

@router.get("/", response_model=List[schemas.PartnerRead])
def list_partners(db: Session = Depends(get_db_with_schema)):
    return db.query(models.Partner).all()


@router.post("/", response_model=schemas.PartnerRead, status_code=201)
def create_partner(partner: schemas.PartnerCreate, db: Session = Depends(get_db_with_schema)):
    db_partner = models.Partner(**partner.dict())
    db.add(db_partner)
    db.commit()
    db.refresh(db_partner)
    return db_partner


@router.get("/{partner_id}", response_model=schemas.PartnerRead)
def get_partner(partner_id: int, db: Session = Depends(get_db_with_schema)):
    partner = db.query(models.Partner).filter(models.Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return partner


@router.put("/{partner_id}", response_model=schemas.PartnerRead)
def update_partner(partner_id: int, partner_update: schemas.PartnerUpdate, db: Session = Depends(get_db_with_schema)):
    partner = db.query(models.Partner).filter(models.Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    update_data = partner_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(partner, key, value)

    db.commit()
    db.refresh(partner)
    return partner


@router.delete("/{partner_id}", status_code=204)
def delete_partner(partner_id: int, db: Session = Depends(get_db_with_schema)):
    partner = db.query(models.Partner).filter(models.Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    db.delete(partner)
    db.commit()
    return None