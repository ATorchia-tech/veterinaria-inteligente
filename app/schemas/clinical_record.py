from datetime import datetime, date
from pydantic import BaseModel, ConfigDict, Field


class ClinicalRecordBase(BaseModel):
    symptoms: str | None = Field(None, example="tos, decaimiento")
    diagnosis: str | None = Field(None, example="resfriado leve")
    treatment: str | None = Field(None, example="reposo, hidratación")
    medications: str | None = Field(None, example="vitaminas")


class ClinicalRecordCreate(ClinicalRecordBase):
    pet_id: int = Field(..., example=1)
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "pet_id": 1,
                "symptoms": "tos, decaimiento",
                "diagnosis": "resfriado leve",
                "treatment": "reposo, hidratación",
                "medications": "vitaminas",
            }
        }
    )


class ClinicalRecordRead(ClinicalRecordBase):
    id: int
    visit_date: date
    created_at: datetime
    updated_at: datetime | None = None
    pet_id: int
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "pet_id": 1,
                "visit_date": "2025-11-11",
                "symptoms": "tos, decaimiento",
                "diagnosis": "resfriado leve",
                "treatment": "reposo, hidratación",
                "medications": "vitaminas",
                "created_at": "2025-11-04T12:00:00+00:00",
                "updated_at": "2025-11-04T12:10:00+00:00",
            }
        },
    )
