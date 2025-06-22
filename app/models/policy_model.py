from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, text, Date, ForeignKey, event
from datetime import date
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.agent_model import Agent

class Policy(Base):
    __tablename__ = "policies"

    id: Mapped[str] = mapped_column(primary_key=True)
    scheme_id: Mapped[str] = mapped_column(ForeignKey("schemes.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    premium_amount: Mapped[int] = mapped_column(nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiry_date: Mapped[date] = mapped_column(Date, nullable=False)
    agent_id: Mapped[str] = mapped_column(ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)

    customer: Mapped["Customer"] = relationship("Customer", back_populates="policies")
    agent: Mapped["Agent"] = relationship("Agent", back_populates="policies")

@event.listens_for(Policy, "before_insert")
def set_policy_id(mapper, connection, target):
    result = connection.execute(
        text("SELECT id FROM policies ORDER BY CAST(SUBSTRING(id FROM 3) AS INTEGER) DESC LIMIT 1")
    ).first()

    next_num = int(result[0].replace("PO", "")) + 1 if result else 1
    target.id = f"PO{next_num}"
