from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.auth.role_checker import employee_required, get_current_user
from app.config.logger_config import func_logger
from app.db.session import get_db
from app.exceptions.orm import (
    DatabaseIntegrityError,
    PlanAlreadyExists,
    PlanNotFound,
    UnauthorizedAccess,
)
from app.models import plan_model
from app.schemas import plan_schema

plan_router = APIRouter(prefix="/plan", tags=["Plans"])


@plan_router.post("/", status_code=status.HTTP_201_CREATED)
def create_plan(
    request: plan_schema.CreatePlan,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):

    func_logger.info("POST /plan - Create new Plan!")

    try:
        existing_plan = (
            db.query(plan_model.Plan)
            .filter(request.name == plan_model.Plan.name)
            .first()
        )
        if existing_plan:
            func_logger.error(f"Plan already exists: {request.name}")
            raise PlanAlreadyExists(
                detail=f"Plan already exists: {request.name}",
            )

        plan_data = request.model_dump()
        if current_user["role"] != "admin" and current_user["role"] != "employee":
            func_logger.error("You dont have the permission to create a plan!")
            raise UnauthorizedAccess()

        plan_data["created_by"] = current_user["user"].id

        new_plan = plan_model.Plan(**plan_data)
        db.add(new_plan)
        db.flush()
        db.commit()
        db.refresh(new_plan)

        return {"message": "New Plan created!", "status": status.HTTP_201_CREATED}

    except SQLAlchemyError:
        db.rollback()
        func_logger.error("❌ Database error during employee creation!")
        raise DatabaseIntegrityError(
            detail="Internal Server Error during employee creation"
        )


@plan_router.get(
    "/all_plans",
    status_code=status.HTTP_200_OK,
    response_model=List[plan_schema.ShowPlan],
)
def get_all_plans(
    db: Session = Depends(get_db), current_user_role: dict = Depends(employee_required)
):
    func_logger.info("GET /plan/all_plans - Get the list of all plans")

    plans = db.query(plan_model.Plan).all()
    return plans


@plan_router.get(
    "/{plan_id}", status_code=status.HTTP_200_OK, response_model=plan_schema.ShowPlan
)
def get_plan_by_id(
    plan_id: str = Path(..., description="ID of the plan"),
    db: Session = Depends(get_db),
    current_user_role: dict = Depends(employee_required),
):
    func_logger.info(f"GET /plan/{plan_id} - Get plan by ID")

    plan = db.query(plan_model.Plan).filter(plan_model.Plan.id == plan_id).first()
    if not plan:
        func_logger.warning(f"Plan not found: {plan_id}")
        raise PlanNotFound()
    return plan


@plan_router.put("/{plan_id}", status_code=status.HTTP_200_OK)
def update_plan(
    plan_id: str,
    request: plan_schema.CreatePlan,
    db: Session = Depends(get_db),
    current_user_role: dict = Depends(employee_required),
):
    func_logger.info(f"PUT /plan/{plan_id} - Update Plan")

    plan = db.query(plan_model.Plan).filter(plan_model.Plan.id == plan_id).first()
    if not plan:
        func_logger.warning(f"Plan not found: {plan_id}")
        raise PlanNotFound()

    update_data = request.model_dump()
    for key, value in update_data.items():
        setattr(plan, key, value)

    try:
        db.commit()
        db.refresh(plan)
        return {"message": "Plan updated successfully"}
    except SQLAlchemyError:
        db.rollback()
        func_logger.error(f"❌ Database error during plan update for ID: {plan_id}")
        raise DatabaseIntegrityError(detail="Internal Server Error during plan update")


@plan_router.delete("/{plan_id}", status_code=status.HTTP_200_OK)
def delete_plan(
    plan_id: str,
    db: Session = Depends(get_db),
    current_user_role: dict = Depends(employee_required),
):
    func_logger.info(f"DELETE /plan/{plan_id} - Delete Plan")

    plan = db.query(plan_model.Plan).filter(plan_model.Plan.id == plan_id).first()
    if not plan:
        func_logger.warning(f"Plan not found: {plan_id}")
        raise PlanNotFound()

    try:
        db.delete(plan)
        db.commit()
        return {"message": "Plan deleted successfully"}
    except SQLAlchemyError:
        db.rollback()
        func_logger.error(f"❌ Database error during plan deletion for ID: {plan_id}")
        raise DatabaseIntegrityError(
            detail="Internal Server Error during plan deletion"
        )
