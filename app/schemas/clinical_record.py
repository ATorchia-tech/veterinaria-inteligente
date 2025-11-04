from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ClinicalRecordBase(BaseModel):
    symptoms: str | None = None
    diagnosis: str | None = None
    treatment: str | None = None
    medications: str | None = None


class ClinicalRecordCreate(ClinicalRecordBase):
    pet_id: int


class ClinicalRecordRead(ClinicalRecordBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    pet_id: int
    model_config = ConfigDict(from_attributes=True)
