from pydantic import BaseModel
from datetime import date
from app.utils.transaction_enum import TransactionType, TransactionStatus
from pydantic import ConfigDict

class TransactionBase(BaseModel):
    policy_id: str
    type: TransactionType
    date: date
    status: TransactionStatus 

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    transaction_id: str

    model_config = ConfigDict(from_attributes=True)
