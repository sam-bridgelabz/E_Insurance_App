from datetime import datetime, timedelta, timezone

from app.config.logger_config import func_logger
from app.schemas.token_schema import TokenData
from jose import JWTError, jwt


class AccessToken:
    def __init__(self, algorithm="HS256", time_expire=30, secret_key=None):
        self.algorithm = algorithm
        self.time_expire = time_expire
        self.secret_key = secret_key

    def create_access_token(self, data: dict,
                            expires_delta: timedelta | None = None):
        print('token')
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.time_expire)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, self.secret_key,
                                 algorithm=self.algorithm)
        return encoded_jwt

    def verify_access_token(self, token: str, credentials_exception):
        try:
            payload = jwt.decode(token, self.secret_key,
                                 algorithms=[self.algorithm])
            user_id = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            func_logger.info("User Authenticated")

            return TokenData(user_id=user_id)

        except JWTError as e:
            print(f"JWT Error: {e}")
            raise credentials_exception
