from datetime import date, datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.schemas.report import AttendanceReport

router = APIRouter()


@router.get("/attendance", response_model=AttendanceReport)
def attendance_report(
    start: date = Query(...),
    end: date = Query(...),
    db: Session = Depends(get_db),
):
    start_dt = datetime(start.year, start.month, start.day)
    end_dt = datetime(end.year, end.month, end.day, 23, 59, 59)
    total = db.query(models.Appointment).filter(
        models.Appointment.date >= start_dt, models.Appointment.date <= end_dt
    )
    attended = total.filter(models.Appointment.status == "attended").count()
    canceled = total.filter(models.Appointment.status == "canceled").count()
    scheduled = total.filter(models.Appointment.status == "scheduled").count()
    return AttendanceReport(
        start=start, end=end, attended=attended, canceled=canceled, scheduled=scheduled
    )
