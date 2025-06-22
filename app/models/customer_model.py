from sqlalchemy import String, ForeignKey, Integer, event, text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import date

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=False)
    dob: Mapped[date] = mapped_column(Date, nullable=False)
    agent_id: Mapped[str] = mapped_column(ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    total_amount: Mapped[int] = mapped_column(Integer, default=0)

    policies = relationship("Policy", back_populates="customer", cascade="all, delete")

@event.listens_for(Customer, "before_insert")
def set_customer_id(mapper, connection, target):
    result = connection.execute(
        text("SELECT id FROM customers ORDER BY CAST(SUBSTRING(id FROM 3) AS INTEGER) DESC LIMIT 1")
    ).first()

    next_num = int(result[0].replace("CU", "")) + 1 if result else 1
    target.id = f"CU{next_num}"
