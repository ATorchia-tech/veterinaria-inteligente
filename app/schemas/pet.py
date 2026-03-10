from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field


class PetBase(BaseModel):
    name: str = Field(..., example="Firulais")
    species: str = Field(..., example="perro")
    breed: str | None = Field(None, example="mestizo")
    birth_date: date | None = Field(None, example="2020-05-01")
    notes: str | None = Field(None, example="vacunas al día")


class PetCreate(PetBase):
    owner_id: int = Field(..., example=1)
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Firulais",
                "species": "perro",
                "breed": "mestizo",
                "birth_date": "2020-05-01",
                "notes": "vacunas al día",
                "owner_id": 1,
            }
        }
    )


class PetRead(PetBase):
    id: int
    owner_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Firulais",
                "species": "perro",
                "breed": "mestizo",
                "birth_date": "2020-05-01",
                "notes": "vacunas al día",
                "owner_id": 1,
                "created_at": "2025-11-04T12:00:00+00:00",
                "updated_at": "2025-11-04T12:00:00+00:00",
            }
        },
    )
