from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field


class VaccinationBase(BaseModel):
    vaccine_name: str = Field(..., json_schema_extra={"example": "Antirrábica"})
    due_date: date = Field(..., json_schema_extra={"example": "2025-12-01"})
    last_date: date | None = Field(None, json_schema_extra={"example": "2024-12-01"})
    status: str | None = Field(None, json_schema_extra={"example": "due"})


class VaccinationCreate(VaccinationBase):
    pet_id: int = Field(..., json_schema_extra={"example": 1})
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "pet_id": 1,
                "vaccine_name": "Antirrábica",
                "due_date": "2025-12-01",
                "last_date": "2024-12-01",
                "status": "due",
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
                "last_date": "2024-12-01",
                "status": "due",
                "created_at": "2025-11-04T12:00:00+00:00",
                "updated_at": "2025-11-04T12:00:00+00:00",
            }
        },
    )
