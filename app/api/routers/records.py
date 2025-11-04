from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.schemas.clinical_record import ClinicalRecordCreate, ClinicalRecordRead

router = APIRouter()


@router.post("/", response_model=ClinicalRecordRead)
def create_record(payload: ClinicalRecordCreate, db: Session = Depends(get_db)):
    pet = db.get(models.Pet, payload.pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    rec = models.ClinicalRecord(
        pet_id=payload.pet_id,
        symptoms=payload.symptoms,
        diagnosis=payload.diagnosis,
        treatment=payload.treatment,
        medications=payload.medications,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


@router.get("/", response_model=List[ClinicalRecordRead])
def list_records(
    pet_id: Optional[int] = Query(default=None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    q = db.query(models.ClinicalRecord).order_by(models.ClinicalRecord.created_at.desc())
    if pet_id is not None:
        q = q.filter(models.ClinicalRecord.pet_id == pet_id)
    return q.offset((page - 1) * page_size).limit(page_size).all()
