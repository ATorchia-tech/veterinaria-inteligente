from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class OwnerBase(BaseModel):
    name: str
    phone: str | None = None
    email: EmailStr | None = None


class OwnerCreate(OwnerBase):
    pass


class OwnerRead(OwnerBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
