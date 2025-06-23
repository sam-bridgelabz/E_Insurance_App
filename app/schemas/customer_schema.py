from pydantic import BaseModel, ConfigDict, EmailStr, constr, Field
from typing import Optional
from datetime import date

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    dob: date

class CustomerCreate(CustomerBase):
    password: str = Field(exclude=True)
    pass

class CustomerResponse(CustomerBase):
    id: str
    total_amount: int
    dob: date

    model_config = ConfigDict(from_attributes=True)

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    dob: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)

