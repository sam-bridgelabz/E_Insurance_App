from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AdminSchema(BaseModel):
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class CreateAdmin(AdminSchema):
    password: str
    model_config = ConfigDict(from_attributes=True)


class ShowAdmin(AdminSchema):
    id: str
    created_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


class UpdateAdmin(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

