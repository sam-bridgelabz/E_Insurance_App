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
    name: Optional[str]
    email: Optional[str]
    dept: Optional[DepartmentEnum]
    password: Optional[str]

    model_config = ConfigDict(from_attributes=True)
