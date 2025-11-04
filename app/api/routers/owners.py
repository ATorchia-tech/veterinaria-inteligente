from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.schemas.owner import OwnerCreate, OwnerRead

router = APIRouter()


@router.post("/", response_model=OwnerRead)
def create_owner(payload: OwnerCreate, db: Session = Depends(get_db)):
    owner = models.Owner(name=payload.name, phone=payload.phone, email=payload.email)
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return owner


@router.get("/", response_model=List[OwnerRead])
def list_owners(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    q = db.query(models.Owner).order_by(models.Owner.id.asc())
    return q.offset((page - 1) * page_size).limit(page_size).all()


@router.get("/{owner_id}", response_model=OwnerRead)
def get_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.get(models.Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    return owner
