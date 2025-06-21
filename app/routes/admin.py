from typing import List

from app.auth.role_checker import admin_required, get_current_user
from app.config.logger_config import func_logger
from app.db.session import get_db
from app.models import admin_model
from app.schemas import admin_schema
from app.utils.hash_password import Hash
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

admin_router = APIRouter(prefix="/admin", tags=["Admin"])


@admin_router.post(
    "/", status_code=status.HTTP_201_CREATED,
    response_model=admin_schema.ShowAdmin
)
def create_admin(
        request: admin_schema.CreateAdmin,
        db: Session = Depends(get_db),
        current_user: dict = Depends(admin_required)
):
    func_logger.info("POST /admin - Create new Admin!")

    try:
        existing_email = (
            db.query(admin_model.Admin)
            .filter(request.email == admin_model.Admin.email)
            .first()
        )
        if existing_email:
            func_logger.error(f"Email already exists: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email already exists: {request.email}",
            )

        admin_data = request.model_dump()
        admin_data["password"] = Hash.get_hash_password(request.password)
        new_user = admin_model.Admin(**admin_data)

        db.add(new_user)
        db.flush()
        db.commit()
        db.refresh(new_user)

        return new_user

    except SQLAlchemyError as e:
        db.rollback()
        func_logger.error("❌ Database error during adding admin!")
        raise HTTPException(
            status_code=500, detail="Internal Server Error during signup"
        )


@admin_router.get(
    "/", status_code=status.HTTP_200_OK,
    response_model=List[admin_schema.ShowAdmin]
)
def get_all_admins(
        db: Session = Depends(get_db),
        current_user: dict = Depends(admin_required)
):
    func_logger.info("GET /admin - Get list of Admins!")
    admins = db.query(admin_model.Admin).all()
    return admins


@admin_router.get("/{id}", status_code=status.HTTP_200_OK,
                  response_model=admin_schema.ShowAdmin)
def get_admin_by_id(
        id: str, db: Session = Depends(get_db),
        current_user: dict = Depends(admin_required)
):
    func_logger.info(f"GET /admin/{id} - Get Admin Details!")
    admin = db.query(admin_model.Admin).filter(
        admin_model.Admin.id == id).first()

    if not admin:
        func_logger.error(f"❌The admin is not present: {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The admin is not present: {id}",
        )

    return admin


@admin_router.put("/", status_code=status.HTTP_202_ACCEPTED)
def update_admin(
        request: admin_schema.UpdateAdmin,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user),
):
    func_logger.info(f"PUT /admin/- Update Admin Details!")

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You aren't allowed to make changes here!"
        )

    try:
        id = current_user["user"].id
        admin = db.query(admin_model.Admin).filter(
            admin_model.Admin.id == id).first()

        if not admin:
            func_logger.error(f"❌The admin is not present: {id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The admin is not present: {id}",
            )

        update_data = request.model_dump(exclude_unset=True)

        if "email" in update_data:
            existing_admin = (
                db.query(admin_model.Admin)
                .filter(admin_model.Admin.email == update_data["email"],
                        admin_model.Admin.id != id)
                .first()
            )
            if existing_admin:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email is already in use by another admin.",
                )

        if "password" in update_data:
            update_data["password"] = Hash.get_hash_password(
                update_data["password"])

        for key, value in update_data.items():
            setattr(admin, key, value)

        db.commit()
        db.refresh(admin)

        func_logger.info(f"✅ Admin updated successfully: {id}")
        return {
            "message": f"Admin updated successfully: {id}",
            "status": status.HTTP_202_ACCEPTED,
        }

    except SQLAlchemyError as e:
        db.rollback()
        func_logger.error("❌ Database error during updation!!")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred in Database during update.",
        )


@admin_router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_admin(
        id: str, db: Session = Depends(get_db),
        current_user: dict = Depends(admin_required)
):
    func_logger.info(f"DELETE /admin/{id} - Delete Admin Details!")
    try:
        admin = db.query(admin_model.Admin).filter(admin_model.Admin.id == id)

        if not admin.first():
            func_logger.error(f"❌The admin is not present: {id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The admin is not present: {id}",
            )

        admin.delete(synchronize_session=False)
        db.commit()

        func_logger.info(f"Admin deleted successfully: {id}")
        return {
            "message": f"Admin deleted successfully: {id}",
            "status": status.HTTP_200_OK,
        }

    except SQLAlchemyError as e:
        db.rollback()
        func_logger.error("❌ Database error during user deletion.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error during user deletion",
        )
