from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class PetBase(BaseModel):
    name: str
    species: str
    breed: str | None = None
    birth_date: date | None = None
    notes: str | None = None


class PetCreate(PetBase):
    owner_id: int


class PetRead(PetBase):
    id: int
    owner_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
