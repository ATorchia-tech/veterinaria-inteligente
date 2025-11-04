from datetime import date, datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.schemas.appointment import AppointmentRead

router = APIRouter()


@router.get("/day", response_model=List[AppointmentRead])
def agenda_diaria(day: Optional[date] = Query(None), db: Session = Depends(get_db)):
    d = day or date.today()
    start = datetime(d.year, d.month, d.day)
    end = start + timedelta(days=1)
    q = (
        db.query(models.Appointment)
        .filter(models.Appointment.date >= start, models.Appointment.date < end)
        .order_by(models.Appointment.date.asc())
    )
    return q.all()
