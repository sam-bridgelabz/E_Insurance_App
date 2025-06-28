from sqlalchemy.orm import Session

from app.models import Admin, Employee


class AdminQueries:

    @staticmethod
    def get_by_email(db: Session, admin_email: str) -> Admin | None:
        return db.query(Admin).filter(Admin.email == admin_email)

    @staticmethod
    def get_by_id(db: Session, admin_id: str) -> Admin | None:
        return db.query(Admin).filter(Admin.id == admin_id)

    @staticmethod
    def check_if_email_is_same(
        db: Session, updated_email: str, admin_id: str
    ) -> Admin | None:
        return db.query(Admin).filter(
            Admin.email == updated_email, Admin.id != admin_id
        )


class EmployeeQueries:

    @staticmethod
    def get_by_email(db: Session, employee_email: str) -> Employee | None:
        return db.query(Employee).filter(Employee.email == employee_email)

    @staticmethod
    def get_by_id(db: Session, employee_id: str) -> Employee | None:
        return db.query(Employee).filter(Employee.id == employee_id)

    @staticmethod
    def check_if_email_is_same(
        db: Session, updated_email: str, employee_id: str
    ) -> Employee | None:
        return db.query(Employee).filter(
            Employee.email == updated_email, Employee.id != employee_id
        )
