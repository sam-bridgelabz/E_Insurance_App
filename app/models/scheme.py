from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  String, Text, DateTime, ForeignKey, JSON
from datetime import datetime
from app.db.base import Base
from sqlalchemy.sql import func


class Scheme(Base):
    __tablename__ = "schemes"

    id: Mapped[str] = mapped_column(primary_key=True, autoincrement=True)

    plan_id: Mapped[str] = mapped_column(
        ForeignKey("plans.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    created_by: Mapped[str] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(),
                                                 nullable=False)

    commission_rule: Mapped[dict] = mapped_column(JSON, nullable=False)

    plan: Mapped["Plan"] = relationship(back_populates="schemes")
