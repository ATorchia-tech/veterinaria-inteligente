from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field


class OwnerBase(BaseModel):
    name: str = Field(..., example="Juan Pérez")
    phone: str | None = Field(None, example="123456")
    email: EmailStr | None = Field(None, example="juan@example.com")


class OwnerCreate(OwnerBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Juan Pérez",
                "phone": "123456",
                "email": "juan@example.com",
            }
        }
    )


class OwnerRead(OwnerBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Juan Pérez",
                "phone": "123456",
                "email": "juan@example.com",
                "created_at": "2025-11-04T12:00:00+00:00",
                "updated_at": "2025-11-04T12:00:00+00:00",
            }
        },
    )
