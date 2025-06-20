# Has all the routes related to the admin

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config.logger_config import func_logger
from app.database import get_db
from app.models import admin_model
from app.schemas import admin_schema
from app.utils.hash_password import Hash

admin_router = APIRouter(prefix="/admin", tags=["Admin"])


# Only an admin can create another admin (Check this during auth)
@admin_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=admin_schema.ShowAdmin
)
def create_admin(request: admin_schema.CreateAdmin, db: Session = Depends(get_db)):
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
        new_user = admin_model.Admin.create(**admin_data)

        db.add(new_user)
        db.flush()
        db.commit()
        db.refresh(new_user)

    except SQLAlchemyError as e:
        db.rollback()
        func_logger.error("❌ Database error during adding admin!")
        raise HTTPException(
            status_code=500, detail="Internal Server Error during signup"
        )


# Get all admins listed
@admin_router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[admin_schema.ShowAdmin]
)
def get_all_admins(db: Session = Depends(get_db)):
    func_logger.info("GET /admin - Get list of Admins!")

    admins = db.query(admin_model.Admin).all()
    return admins


# Get admin by ID
@admin_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_admin_by_id(id: str, db: Session = Depends(get_db)):
    func_logger.info(f"GET /admin{id} - Get Admin Details!")
    admin = db.query(admin_model.Admin).filter(admin_model.Admin.id == id).first()

    if not admin:
        func_logger.error(f"❌The admin is not present: {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            details=f"The admin is not present: {id}",
        )

    return admin


# Update the details of the admin
@admin_router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_admin(
    id: str, request: admin_schema.UpdateAdmin, db: Session = Depends(get_db)
):

    func_logger.info(f"PUT /admin/{id} - Update Admin Details!")

    try:
        admin = db.query(admin_model.Admin).filter(admin_model.Admin.id == id)
        if not admin.first():
            func_logger.error(f"❌The admin is not present: {id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                details=f"The admin is not present: {id}",
            )

        update_data = request.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password"] = Hash.get_hash_password(update_data["password"])

        admin.update(update_data)

        db.commit()

        func_logger.info(f"Admin updated successfully: {id}")
        return {
            "meesage": f"Admin updated successfully: {id}",
            "payload": admin,
            "status": status.HTTP_202_ACCEPTED,
        }

    except SQLAlchemyError as e:
        db.rollback()
        func_logger.error("❌ Database error during updation!!")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occured in Database during update.",
        )


# Delete admin
@admin_router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_admin(id: str, db: Session = Depends(get_db)):
    func_logger.info(f"DELETE /admin/{id} - Delete Admin Details!")
    try:
        admin = db.query(admin_model.Admin).filter(admin_model.Admin.id == id)

        if not admin.first():
            func_logger.error(f"❌The admin is not present: {id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                details=f"The admin is not present: {id}",
            )

        admin.delete(synchronize_session=False)
        db.commit()

        func_logger(f"User deleted successfully: {id}")
        return {
            "meesage": f"Admin deleted successfully: {id}",
            "payload": admin,
            "status": status.HTTP_202_ACCEPTED,
        }

    except SQLAlchemyError as e:
        db.rollback()
        func_logger.error("❌ Database error during user deletion.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error during user deletion",
        )
