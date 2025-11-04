from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AppointmentBase(BaseModel):
    date: datetime
    reason: str


class AppointmentCreate(AppointmentBase):
    pet_id: int


class AppointmentRead(AppointmentBase):
    id: int
    status: str
    pet_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
