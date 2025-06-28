from datetime import date

from pydantic import BaseModel, ConfigDict


class PolicyCreate(BaseModel):
    scheme_id: str
    name: str
    customer_id: str
    premium_amount: int
    start_date: date
    expiry_date: date


class PolicyResponse(PolicyCreate):
    id: str
    agent_id: str

    model_config = ConfigDict(from_attributes=True)
