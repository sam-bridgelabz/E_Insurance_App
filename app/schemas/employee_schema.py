from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.utils.department_enum import DepartmentEnum


class EmpSchema(BaseModel):
    name: str
    email: str
    dept: DepartmentEnum

    model_config = ConfigDict(from_attributes=True)


class CreateEmployee(EmpSchema):
    password: str
    model_config = ConfigDict(from_attributes=True)


class ShowEmployee(EmpSchema):
    id: str
    admin_id: str
    doj: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateEmployee(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    dept: Optional[DepartmentEnum] = None
    password: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
