from typing import List

from app.auth.role_checker import admin_required
from app.config.logger_config import func_logger
from app.db.session import get_db
from app.models import employee_model
from app.schemas import employee_schema
from app.utils.hash_password import Hash
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.exceptions.orm import DatabaseIntegrityError, EmailAlreadyExists, EmployeeNotFound
from app.queries.user_queries import EmployeeQueries

employee_router = APIRouter(prefix="/employee", tags=["Employee"])


@employee_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=employee_schema.ShowEmployee,
)
def create_employee(
        request: employee_schema.CreateEmployee,
        db: Session = Depends(get_db),
        current_user: dict = Depends(admin_required),
):
    func_logger.info("POST /employee - Create new Employee!")
    try:
        existing_email = EmployeeQueries.get_by_email(db, request.email).first()
        
        if existing_email:
            func_logger.error(f"Email already exists: {request.email}")
            raise EmailAlreadyExists(
                detail=f"Email already exists: {request.email}",
            )

        emp_data = request.model_dump()
        emp_data["password"] = Hash.get_hash_password(request.password)
        emp_data["admin_id"] = current_user["user"].id

        new_emp = employee_model.Employee(**emp_data)

        db.add(new_emp)
        db.flush()
        db.commit()
        db.refresh(new_emp)

        return new_emp

    except SQLAlchemyError as e:
        db.rollback()
        func_logger.error("❌ Database error during employee creation!")
        raise DatabaseIntegrityError(
            detail="Internal Server Error during employee creation"
        )


@employee_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[employee_schema.ShowEmployee],
)
def get_all_employees(
        db: Session = Depends(get_db),
        current_user: dict = Depends(admin_required)
):
    func_logger.info("GET /employee - Get list of Employees!")
    employees = db.query(employee_model.Employee).all()
    return employees


@employee_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_employee_by_id(
        id: str, db: Session = Depends(get_db),
        current_user: dict = Depends(admin_required)
):
    func_logger.info(f"GET /employee/{id} - Get Employee Details!")
    emp = EmployeeQueries.get_by_id(db, id).first()


    if not emp:
        func_logger.error(f"❌The employee is not present: {id}")
        raise EmployeeNotFound(
            detail=f"The employee is not present: {id}"
        )

    return emp


@employee_router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_employee(
        id: str,
        request: employee_schema.UpdateEmployee,
        db: Session = Depends(get_db),
        current_user: dict = Depends(admin_required),
):
    func_logger.info(f"PUT /employee/{id} - Update Employee Details!")

    try:
        emp = EmployeeQueries.get_by_id(db, id)
        if not emp.first():
            func_logger.error(f"❌The employee is not present: {id}")
            raise EmployeeNotFound(
                detail=f"The employee is not present: {id}"
            )

        update_data = request.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password"] = Hash.get_hash_password(
                update_data["password"])

        emp.update(update_data)
        db.commit()

        func_logger.info(f"Employee updated successfully: {id}")
        return {
            "message": f"Employee updated successfully: {id}",
            "status": status.HTTP_202_ACCEPTED,
        }

    except SQLAlchemyError as e:
        db.rollback()
        func_logger.error("❌ Database error during employee update!")
        raise DatabaseIntegrityError(
            detail="Error occurred in Database during update."
        )


@employee_router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_employee(
        id: str, db: Session = Depends(get_db),
        current_user: dict = Depends(admin_required)
):
    func_logger.info(f"DELETE /employee/{id} - Delete Employee!")
    try:
        emp = EmployeeQueries.get_by_id(db, id)

        if not emp.first():
            func_logger.error(f"❌The employee is not present: {id}")
            raise EmployeeNotFound(
                detail=f"The employee is not present: {id}"
            )

        emp.delete(synchronize_session=False)
        db.commit()

        func_logger.info(f"Employee deleted successfully: {id}")
        return {
            "message": f"Employee deleted successfully: {id}",
            "status": status.HTTP_200_OK,
        }

    except SQLAlchemyError as e:
        db.rollback()
        func_logger.error("❌ Database error during employee deletion.")
        raise DatabaseIntegrityError(
            detail="Internal Server Error during employee deletion"
        )
