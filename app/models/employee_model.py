from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Date
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, String, event, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.utils.department_enum import DepartmentEnum

if TYPE_CHECKING:
    from app.models.admin_model import Admin
    from app.models.agent_model import Agent


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    admin_id: Mapped[str] = mapped_column(String(20), ForeignKey("admins.id"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    dept: Mapped[DepartmentEnum] = mapped_column(
        SQLAlchemyEnum(DepartmentEnum), nullable=False
    )
    doj: Mapped[datetime] = mapped_column(default=datetime.now)

    admin: Mapped["Admin"] = relationship("Admin", back_populates="employees")
    agents: Mapped[List["Agent"]] = relationship(
        "Agent", back_populates="emp", cascade="all, delete-orphan"
    )


@event.listens_for(Employee, "before_insert")
def get_employee_id(mapper, connection, target):
    result = connection.execute(
        text(
            "SELECT id from employees ORDER BY CAST(SUBSTRING(id FROM 3) AS INTEGER) DESC LIMIT 1"
        )
    ).first()
    if result is None:
        next_num = 1
    else:
        last_id = result[0]
        last_num = int(last_id.replace("EM", ""))
        next_num = last_num + 1

    target.id = f"EM{next_num}"
