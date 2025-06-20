from typing import Optional

from pydantic import BaseModel, ConfigDict


class AgentSchema(BaseModel):
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class CreateAgent(AgentSchema):
    password: str

    model_config = ConfigDict(from_attributes=True)


class ShowAgent(AgentSchema):
    id: str
    emp_id: str

    model_config = ConfigDict(from_attributes=True)


class UpdateAgent(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]

    model_config = ConfigDict(from_attributes=True)
