from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.auth.oauth2 import get_current_user
from app.auth.token import AccessToken
from app.config.load_config import api_settings
from app.config.logger_config import func_logger  # <-- Add this
from app.db.session import get_db
from app.exceptions.orm import (
    DatabaseIntegrityError,
    InvalidCredentialsException,
    TokenCreationError,
)
from app.models import admin_model, agent_model, employee_model
from app.schemas.admin_schema import ShowAdmin
from app.utils.hash_password import Hash

user_router = APIRouter(tags=["User"])
login_router = APIRouter(tags=["Login"])


@user_router.get("/me", response_model=ShowAdmin)
def get_user(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    func_logger.info(f"User data fetched for ID: {current_user['user'].id}")
    if not current_user["user"].created_at:  # temporary fix
        current_user["user"].created_at = None
    return current_user["user"]


@login_router.post("/auth/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    email = request.username
    password = request.password

    func_logger.info(f"Login attempt for email: {email}")

    try:
        user = (
            db.query(admin_model.Admin).filter(admin_model.Admin.email == email).first()
            or db.query(employee_model.Employee)
            .filter(employee_model.Employee.email == email)
            .first()
            or db.query(agent_model.Agent)
            .filter(agent_model.Agent.email == email)
            .first()
        )

        if not user:
            func_logger.warning(f"Login failed — user not found: {email}")
            raise InvalidCredentialsException()

        if not Hash.verify_password(password, user.password):
            func_logger.warning(f"Login failed — incorrect password for: {email}")
            raise InvalidCredentialsException()

        try:
            token_obj = AccessToken(time_expire=30, secret_key=api_settings.SECRET_KEY)
            access_token = token_obj.create_access_token(data={"sub": str(user.id)})
            func_logger.info(f"Token generated for user ID: {user.id}")
            return {"access_token": access_token, "token_type": "bearer"}

        except Exception as e:
            func_logger.error(f"Token creation failed for user ID {user.id}: {e}")
            raise TokenCreationError()

    except SQLAlchemyError as e:
        func_logger.error(f"Database error during login for {email}: {e}")
        raise DatabaseIntegrityError(detail=f"Database error during login, {e}")
