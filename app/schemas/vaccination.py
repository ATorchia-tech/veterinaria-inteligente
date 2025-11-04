from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class VaccinationBase(BaseModel):
    vaccine_name: str
    due_date: date
    last_date: date | None = None
    status: str | None = None


class VaccinationCreate(VaccinationBase):
    pet_id: int


class VaccinationRead(VaccinationBase):
    id: int
    pet_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
