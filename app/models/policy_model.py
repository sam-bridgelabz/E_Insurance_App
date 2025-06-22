from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, text, Date, ForeignKey, event
from datetime import date
from app.db.base import Base


class Policy(Base):
    __tablename__ = "policies"

    id: Mapped[str] = mapped_column(primary_key=True)

    scheme_id: Mapped[str] = mapped_column(
        ForeignKey("schemes.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    customer_id: Mapped[str] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"), nullable=False
    )
    premium_amount: Mapped[int] = mapped_column(nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiry_date: Mapped[date] = mapped_column(Date, nullable=False)
    agent_id: Mapped[str] = mapped_column(
        ForeignKey("agents.id", ondelete="CASCADE"), nullable=False
    )
    agent: Mapped["Agent"] = relationship("Agent", back_populates="policies")


@event.listens_for(Policy, "before_insert")
def get_agent_id(mapper, connection, target):
    result = connection.execute(
        text(
            "SELECT id FROM policies ORDER BY CAST(SUBSTRING(id FROM 3) AS INTEGER) DESC LIMIT 1"
        )
    ).first()

    if result is None:
        next_num = 1
    else:
        last_id = result[0]
        last_num = int(last_id.replace("PO", ""))
        next_num = last_num + 1

    target.id = f"PO{next_num}"
