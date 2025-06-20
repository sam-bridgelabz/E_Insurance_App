from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.oauth2 import get_current_user
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.auth.token import AccessToken
from app.database import get_db
from app.models import admin_model, employee_model, agent_model
from ..utils.exceptions import (
    InvalidCredentialsException,
    TokenCreationError,
    DatabaseIntegrityError,
)
from ..utils.hashing import Hash
from app.config.settings import authSettings

user_router = APIRouter(tags=["User"])
login_router = APIRouter(tags=["Login"])


@user_router.get("/me")
def get_user(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return {"message": "Current user details", "payload": current_user, "status_code": 200}


@login_router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    try:
        email = request.username
        password = request.password

        user = (
            db.query(admin_model.Admin).filter(admin_model.Admin.email == email).first()
            or db.query(employee_model.Employee)
            .filter(employee_model.Employee.email == email)
            .first()
            or db.query(agent_model.Agent)
            .filter(agent_model.Agent.email == email)
            .first()
        )

        if not user or not Hash.verify(password, user.password):
            raise InvalidCredentialsException()

        try:
            token_obj = AccessToken(time_expire=30, secret_key=authSettings.SECRET_KEY)
            access_token = token_obj.create_access_token(
                data={
                    "sub": user.id,
                }
            )
            return {"access_token": access_token, "token_type": "bearer"}

        except Exception:
            raise TokenCreationError(detail="Failed to generate authentication token")

    except SQLAlchemyError as e:
        raise DatabaseIntegrityError(detail=f"Database error during login, {e}")
