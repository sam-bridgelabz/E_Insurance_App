from datetime import datetime
from typing import List, TYPE_CHECKING

from app.db.base import Base
from sqlalchemy import  Integer, String, cast, event, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text


if TYPE_CHECKING:
    from app.models.employee_model import Employee


class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[str] = mapped_column(
        String(20), primary_key=True, nullable=False, unique=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    employees: Mapped[List["Employee"]] = relationship(
        "Employee", back_populates="admin", cascade="all, delete-orphan"
    )



@event.listens_for(Admin, "before_insert")
def set_admin_id(mapper, connection, target):
    result = connection.execute(
        text(
            "SELECT id FROM admins ORDER BY CAST(SUBSTRING(id FROM 3) AS INTEGER) DESC LIMIT 1"
        )
    ).first()
    if result is None:
        next_num = 1
    else:
        last_id = result[0]
        last_num = int(last_id.replace("AD", ""))
        next_num = last_num + 1

    target.id = f"AD{next_num}"
