from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

from pydantic import ConfigDict


class SchemeCreate(BaseModel):
    plan_id: str
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class SchemeRead(SchemeCreate):
    id: str
    created_by: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SchemeSuccessResponse(BaseModel):
    message: str
    status: int
    payload: SchemeRead


class SchemeDeleteResponse(BaseModel):
    message: str
    status: int
