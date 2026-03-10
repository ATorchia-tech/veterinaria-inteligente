from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class AppointmentBase(BaseModel):
    date: datetime = Field(..., example="2025-11-04T15:00:00")
    reason: str = Field(..., example="control anual")


class AppointmentCreate(AppointmentBase):
    pet_id: int = Field(..., example=1)
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "date": "2025-11-04T15:00:00",
                "reason": "control anual",
                "pet_id": 1,
            }
        }
    )


class AppointmentRead(AppointmentBase):
    id: int
    status: str
    pet_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "date": "2025-11-04T15:00:00",
                "reason": "control anual",
                "status": "scheduled",
                "pet_id": 1,
                "created_at": "2025-11-04T12:00:00+00:00",
                "updated_at": "2025-11-04T12:00:00+00:00",
            }
        },
    )
