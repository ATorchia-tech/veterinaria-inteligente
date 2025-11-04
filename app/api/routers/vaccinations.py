from datetime import date, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.schemas.vaccination import VaccinationCreate, VaccinationRead

router = APIRouter()


@router.post("/", response_model=VaccinationRead)
def create_vaccination(payload: VaccinationCreate, db: Session = Depends(get_db)):
    pet = db.get(models.Pet, payload.pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    v = models.Vaccination(
        pet_id=payload.pet_id,
        vaccine_name=payload.vaccine_name,
        due_date=payload.due_date,
        last_date=payload.last_date,
        status=payload.status or "due",
    )
    db.add(v)
    db.commit()
    db.refresh(v)
    return v


@router.get("/upcoming", response_model=List[VaccinationRead])
def upcoming(
    days: int = Query(30, ge=1, le=365),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    today = date.today()
    limit = today + timedelta(days=days)
    q = (
        db.query(models.Vaccination)
        .filter(models.Vaccination.due_date >= today, models.Vaccination.due_date <= limit)
        .order_by(models.Vaccination.due_date.asc())
    )
    return q.offset((page - 1) * page_size).limit(page_size).all()
