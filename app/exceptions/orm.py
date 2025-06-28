from fastapi import HTTPException, status


class AdminNotFound(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: str = "Admin not found",
    ):
        super().__init__(status_code=status_code, detail=detail)


class AdminAlreadyExists(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_409_CONFLICT,
        detail: str = "Admin Already Exists",
    ):
        super().__init__(status_code=status_code, detail=detail)


class EmailAlreadyExists(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_409_CONFLICT,
        detail: str = "Email Already Exists",
    ):
        super().__init__(status_code=status_code, detail=detail)


class AgentNotFound(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: str = "Agent not found",
    ):
        super().__init__(status_code=status_code, detail=detail)


class EmployeeNotFound(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: str = "Employee not found",
    ):
        super().__init__(status_code=status_code, detail=detail)


class PlanAlreadyExists(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_409_CONFLICT,
        detail: str = "Plan Already Exists",
    ):
        super().__init__(status_code=status_code, detail=detail)


class PlanNotFound(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: str = "Plan not found",
    ):
        super().__init__(status_code=status_code, detail=detail)


class SchemeNotFound(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: str = "Scheme not found",
    ):
        super().__init__(status_code=status_code, detail=detail)


class SchemeAlreadyExists(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_409_CONFLICT,
        detail: str = "Scheme already exists",
    ):
        super().__init__(status_code=status_code, detail=detail)


class PolicyAlreadyExists(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_409_CONFLICT,
        detail: str = "Plan already exists",
    ):
        super().__init__(status_code=status_code, detail=detail)


class UnauthorizedAccess(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_403_FORBIDDEN,
        detail: str = "Access denied",
    ):
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


class ExpiryDateError(HTTPException):
    def __init__(self, status_code, detail=None, headers=None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expiry date must be after start date.",
        )


class ZeroAmountError(HTTPException):
    def __init__(self, status_code, detail=None, headers=None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Premium amount must be greater than 0.",
        )


class PolicyNotFound(HTTPException):
    def __init__(self, status_code, detail=None, headers=None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy Not Found",
        )


class CustomerNotFound(HTTPException):
    def __init__(self, status_code, detail=None, headers=None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer Not Found",
        )
