from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.schemas.appointment import AppointmentCreate, AppointmentRead

router = APIRouter()


@router.post("/", response_model=AppointmentRead)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    pet = db.get(models.Pet, payload.pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    ap = models.Appointment(
        date=payload.date,
        reason=payload.reason,
        status="scheduled",
        pet_id=payload.pet_id,
    )
    db.add(ap)
    db.commit()
    db.refresh(ap)
    return ap


@router.get("/", response_model=List[AppointmentRead])
def list_appointments(db: Session = Depends(get_db)):
    return db.query(models.Appointment).order_by(models.Appointment.date.asc()).all()


@router.post("/{appointment_id}/cancel", response_model=AppointmentRead)
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    ap = db.get(models.Appointment, appointment_id)
    if not ap:
        raise HTTPException(status_code=404, detail="Appointment not found")
    ap.status = "canceled"
    db.commit()
    db.refresh(ap)
    return ap
