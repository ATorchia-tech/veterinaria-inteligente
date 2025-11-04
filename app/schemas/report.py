from datetime import date
from pydantic import BaseModel


class AttendanceReport(BaseModel):
    start: date
    end: date
    attended: int
    canceled: int
    scheduled: int
