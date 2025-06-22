from typing import TYPE_CHECKING, List

from app.db.base import Base
from sqlalchemy import ForeignKey, String, event, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.employee_model import Employee
    from app.models.policy_model import Policy


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    emp_id: Mapped[str] = mapped_column(String(20), ForeignKey("employees.id"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False,
                                       unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    emp: Mapped["Employee"] = relationship("Employee", back_populates="agents")
    policies: Mapped[List["Policy"]] = relationship("Policy", back_populates="agent", cascade="all, delete-orphan")
    

@event.listens_for(Agent, "before_insert")
def get_agent_id(mapper, connection, target):
    result = connection.execute(
        text(
            "SELECT id FROM agents ORDER BY CAST(SUBSTRING(id FROM 3) AS INTEGER) DESC LIMIT 1"
        )
    ).first()

    if result is None:
        next_num = 1
    else:
        last_id = result[0]
        last_num = int(last_id.replace("IA", ""))
        next_num = last_num + 1

    target.id = f"IA{next_num}"
