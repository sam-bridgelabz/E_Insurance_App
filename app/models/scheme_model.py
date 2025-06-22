from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, DateTime, ForeignKey, JSON, event, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.plan_model import Plan


class Scheme(Base):
    __tablename__ = "schemes"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)

    plan_id: Mapped[str] = mapped_column(
        ForeignKey("plans.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_by: Mapped[str] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    commission_rule: Mapped[dict] = mapped_column(JSON, nullable=False)

    plan = relationship("Plan", back_populates="schemes")


@event.listens_for(Scheme, "before_insert")
def get_scheme_id(mapper, connection, target):
    result = connection.execute(
        text(
            "SELECT id FROM schemes ORDER BY CAST(SUBSTRING(id FROM 3) AS INTEGER) DESC LIMIT 1"
        )
    ).first()

    next_num = int(result[0].replace("SC", "")) + 1 if result else 1
    target.id = f"SC{next_num}"
