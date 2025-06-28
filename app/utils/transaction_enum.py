import enum


class TransactionType(str, enum.Enum):
    purchase = "purchase"
    renewal = "renewal"


class TransactionStatus(str, enum.Enum):
    success = "success"
    failed = "failed"
    pending = "pending"
