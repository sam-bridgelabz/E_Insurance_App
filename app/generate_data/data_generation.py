from datetime import datetime
from random import choice

from faker import Faker
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, get_db
from app.models.admin_model import Admin
from app.models.agent_model import Agent
from app.models.employee_model import Employee
from app.utils.hash_password import Hash

fake = Faker()


def create_fake_admins(n: int, db: Session):
    for _ in range(n):
        admin = Admin(
            name=fake.name(),
            email=fake.unique.email(),
            password=Hash.get_hash_password("admin"),
            created_at=datetime.now(),
        )
        db.add(admin)

    db.commit()
    print(f"{n} fake admins created.")


def create_fake_emp(n: int, db: Session):
    for _ in range(n):
        emp = Employee(
            name=fake.name(), email=fake.email(), password=Hash.get_hash_password("emp")
        )
        db.add(emp)
    db.commit()

    print(f"{n} fake employees created.")


def create_fake_agent(n: int, db: Session):
    emp_ids = db.query(Employee.id).all()
    if not emp_ids:
        print("No employees found. Create employees first.")
        return

    for _ in range(n):
        agent = Agent(
            name=fake.name(),
            email=fake.email(),
            password=Hash.get_hash_password("agent"),
            empi_id=choice(emp_ids)[0],
        )
        db.add(agent)
    db.commit()
    print(f"{n} fake agents created!!")


if __name__ == "__main__":

    db = SessionLocal()
    try:
        create_fake_admins(3, db)
        print("Created Data")
    finally:
        db.close()
