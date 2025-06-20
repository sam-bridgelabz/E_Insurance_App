from fastapi import HTTPException, status


class credentials_exception(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials entered!!",
            headers={"WWW-Authenticate": "Bearer"},
        )


class TokenCreationError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create authentication token",
        )


class DatabaseIntegrityError(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail or "Database integrity error occurred",
        )


class RequiredEnvVarError(Exception):
    def __init__(self, var_name: str):
        super().__init__(f"Required environment variable '{var_name}' is not set")
        self.var_name = var_name
