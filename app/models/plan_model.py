from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String, event, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.scheme_model import Scheme


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[str] = mapped_column(
        String(20), primary_key=True, nullable=False, unique=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    commission_floor: Mapped[int] = mapped_column(Integer, nullable=False)
    commission_ceil: Mapped[int] = mapped_column(Integer, nullable=False)
    created_by: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    schemes: Mapped[List["Scheme"]] = relationship(
        "Scheme", back_populates="plan", cascade="all, delete-orphan"
    )


@event.listens_for(Plan, "before_insert")
def get_plan_id(mapper, connection, target):
    result = connection.execute(
        text(
            "SELECT id FROM plans ORDER BY CAST(SUBSTRING(id FROM 3) AS INTEGER) DESC LIMIT 1"
        )
    ).first()

    next_num = int(result[0].replace("PL", "")) + 1 if result else 1
    target.id = f"PL{next_num}"
