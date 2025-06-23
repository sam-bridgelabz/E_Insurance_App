from sqlalchemy import String, ForeignKey, Date, Enum, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import event
from datetime import date, datetime
from app.db.base import Base
from app.utils.transaction_enum import TransactionType, TransactionStatus


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[str] = mapped_column(primary_key=True)
    policy_id: Mapped[str] = mapped_column(ForeignKey("policies.id", ondelete="CASCADE"), nullable=False)
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType), nullable=False)
    date: Mapped[datetime] = mapped_column(Date, default=datetime.now())
    status: Mapped[TransactionStatus] = mapped_column(Enum(TransactionStatus), default=TransactionStatus.pending)

    policy = relationship("Policy", back_populates="transactions")
    commission = relationship("Commission", back_populates="transaction", cascade="all, delete", uselist=False)
    


@event.listens_for(Transaction, "before_insert")
def set_transaction_id(mapper, connection, target):
    result = connection.execute(
        text("SELECT transaction_id FROM transactions ORDER BY CAST(SUBSTRING(transaction_id FROM 3) AS INTEGER) DESC LIMIT 1")
    ).first()
    next_num = int(result[0].replace("TR", "")) + 1 if result else 1
    target.transaction_id = f"TR{next_num}"
