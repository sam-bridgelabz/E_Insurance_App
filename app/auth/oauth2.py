from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.utils.exceptions import credentials_exception
from app.config.logger_config import func_logger
from app.models import admin_model, employee_model, agent_model
from app.auth.token import AccessToken
from app.config.settings import authSettings


from database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:
        token_obj = AccessToken(secret_key=authSettings.SECRET_KEY)
        token_data = token_obj.verify_access_token(token, credentials_exception)

        user_id = token_data.user_id

        if not user_id:
            raise credentials_exception

        if user_id.startswith("AD"):
            user = (
                db.query(admin_model.Admin)
                .filter(admin_model.Admin.id == user_id)
                .first()
            )
            role = "admin"
        elif user_id.startswith("EM"):
            user = (
                db.query(employee_model.Employee)
                .filter(employee_model.Employee.id == user_id)
                .first()
            )
            role = "employee"
        elif user_id.startswith("IA"):
            user = (
                db.query(agent_model.Agent)
                .filter(agent_model.Agent.id == user_id)
                .first()
            )
            role = "agent"
        else:
            raise credentials_exception

        return {"user": user, "role": role}

    except JWTError as e:
        func_logger.error(f"JWT Error in get_current_user: {e}")
        raise credentials_exception
