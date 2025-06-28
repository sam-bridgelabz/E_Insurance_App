from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.orm import SchemeAlreadyExists, SchemeNotFound, UnauthorizedAccess


def scheme_not_found_handler(request: Request, exc: SchemeNotFound) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "status": exc.status_code},
    )


def scheme_already_exists_handler(
    request: Request, exc: SchemeAlreadyExists
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "status": exc.status_code},
    )


def unauthorized_access_handler(
    request: Request, exc: UnauthorizedAccess
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "status": exc.status_code},
    )
