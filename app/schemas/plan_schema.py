from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class Plan(BaseModel):
    name: str
    description: str
    commission_floor: int
    commission_ceil: int
    
    model_config = ConfigDict(from_attributes=True)
    
class CreatePlan(Plan):
    created_by: str
    
class ShowPlan(Plan):
    id: str
    created_at: datetime

class UpdatePlan(BaseModel):
    name: Optional[str]
    description: Optional[str]
    commission_floor: Optional[int]
    commission_ceil: Optional[int]