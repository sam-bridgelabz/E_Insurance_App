from datetime import date

from pydantic import BaseModel, ConfigDict

from app.utils.transaction_enum import TransactionStatus, TransactionType


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
