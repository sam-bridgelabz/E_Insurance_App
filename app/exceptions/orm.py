from fastapi import HTTPException, status


class SchemeNotFound(HTTPException):
    def __init__(self, status_code: int = status.HTTP_404_NOT_FOUND,
                 detail: str = "Scheme not found"):
        super().__init__(status_code=status_code, detail=detail)


class SchemeAlreadyExists(HTTPException):
    def __init__(self, status_code: int = status.HTTP_409_CONFLICT,
                 detail: str = "Scheme already exists"):
        super().__init__(status_code=status_code, detail=detail)


class UnauthorizedAccess(HTTPException):
    def __init__(self, status_code: int = status.HTTP_403_FORBIDDEN,
                 detail: str = "Access denied"):
        super().__init__(status_code=status_code, detail=detail)


class CredentialsException(HTTPException):
    def __init__(self):
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
