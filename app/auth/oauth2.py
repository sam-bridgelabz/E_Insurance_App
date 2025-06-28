from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.auth.token import AccessToken
from app.config.load_config import api_settings
from app.config.logger_config import func_logger
from app.db.session import get_db
from app.exceptions.orm import CredentialsException
from app.models import admin_model, agent_model, employee_model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:
        print("func")
        token_obj = AccessToken(secret_key=api_settings.SECRET_KEY)
        token_data = token_obj.verify_access_token(token, CredentialsException)

        user_id = token_data.user_id

        if not user_id:
            raise CredentialsException

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
            raise CredentialsException

        return {"user": user, "role": role}

    except JWTError as e:
        func_logger.error(f"JWT Error in get_current_user: {e}")
        raise CredentialsException
