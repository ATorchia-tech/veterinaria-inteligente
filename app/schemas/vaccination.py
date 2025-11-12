from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field


class VaccinationBase(BaseModel):
    vaccine_name: str = Field(..., example="Antirrábica")
    due_date: date = Field(..., example="2025-12-01")
    applied_date: date = Field(..., example="2024-12-01")
    notes: str | None = Field(None, example="Primera dosis")


class VaccinationCreate(VaccinationBase):
    pet_id: int = Field(..., example=1)
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "pet_id": 1,
                "vaccine_name": "Antirrábica",
                "due_date": "2025-12-01",
                "applied_date": "2024-12-01",
                "notes": "Primera dosis",
            }
        }
    )


class VaccinationRead(VaccinationBase):
    id: int
    pet_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "pet_id": 1,
                "vaccine_name": "Antirrábica",
                "due_date": "2025-12-01",
                "applied_date": "2024-12-01",
                "notes": "Primera dosis",
                "created_at": "2025-11-04T12:00:00+00:00",
                "updated_at": "2025-11-04T12:00:00+00:00",
            }
        },
    )
