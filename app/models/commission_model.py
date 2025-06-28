from sqlalchemy import Float, ForeignKey, String, event, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.transaction_model import Transaction


class Commission(Base):
    __tablename__ = "commissions"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    txn_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("transactions.transaction_id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    commission_amt: Mapped[Float] = mapped_column(Float)

    transaction = relationship("Transaction", back_populates="commission")


@event.listens_for(Commission, "before_insert")
def get_commission_id(mapper, connection, target):
    result = connection.execute(
        text(
            "SELECT id FROM commissions ORDER BY CAST(SUBSTRING(id FROM 3) AS INTEGER) DESC LIMIT 1"
        )
    ).first()

    if result is None:
        next_num = 1
    else:
        last_id = result[0]
        last_num = int(last_id.replace("CM", ""))
        next_num = last_num + 1

    target.id = f"CM{next_num}"
