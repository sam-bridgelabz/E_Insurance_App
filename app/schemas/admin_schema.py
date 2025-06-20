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
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UpdateAdmin(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]

    model_config = ConfigDict(from_attributes=True)
