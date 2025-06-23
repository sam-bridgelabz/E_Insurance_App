from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.auth.oauth2 import get_current_user
from app.db.session import get_db
from app.models.scheme_model import Scheme
from app.schemas.scheme_schema import (
    SchemeCreate, SchemeRead, SchemeSuccessResponse, SchemeDeleteResponse
)
from app.queries.scheme import SchemeQueries
from app.exceptions.orm import SchemeNotFound, SchemeAlreadyExists, \
    UnauthorizedAccess

scheme_router = APIRouter(
    prefix="/api/schemes",
    tags=["Scheme"]
)


def ensure_admin_or_employee(current_user: dict):
    if current_user["role"] not in {"admin", "employee"}:
        raise UnauthorizedAccess(status_code=403,
                                 detail="Access denied: Only admin or employee allowed")


@scheme_router.post("/create", response_model=SchemeSuccessResponse,
                    status_code=status.HTTP_201_CREATED)
async def create_scheme(scheme_data: SchemeCreate,
                        db: Session = Depends(get_db),
                        current_user: dict = Depends(get_current_user)):
    ensure_admin_or_employee(current_user)

    existing = SchemeQueries.get_by_name(db, scheme_data.name)
    if existing:
        raise SchemeAlreadyExists(status_code=400,
                                  detail="Scheme already exists")

    scheme = Scheme(
        plan_id=scheme_data.plan_id,
        name=scheme_data.name,
        description=scheme_data.description,
        created_by=current_user["user"].id
    )
    db.add(scheme)
    db.commit()
    db.refresh(scheme)

    return SchemeSuccessResponse(
        message="Scheme Created Successfully",
        payload=SchemeRead.model_validate(scheme),
        status=status.HTTP_201_CREATED
    )


@scheme_router.get("/{scheme_id}", response_model=SchemeSuccessResponse)
async def get_scheme(scheme_id: str, db: Session = Depends(get_db),
                     current_user: dict = Depends(get_current_user)):
    ensure_admin_or_employee(current_user)

    scheme = SchemeQueries.get_by_id(db, scheme_id)
    if not scheme:
        raise SchemeNotFound(status_code=404, detail="Scheme not found")

    return SchemeSuccessResponse(
        message="Scheme Retrieved Successfully",
        payload=SchemeRead.model_validate(scheme),
        status=status.HTTP_200_OK
    )


@scheme_router.delete("/{scheme_id}", response_model=SchemeDeleteResponse)
async def delete_scheme(scheme_id: str, db: Session = Depends(get_db),
                        current_user: dict = Depends(get_current_user)):
    ensure_admin_or_employee(current_user)

    scheme = SchemeQueries.get_by_id(db, scheme_id)
    if not scheme:
        raise SchemeNotFound(status_code=404, detail="Scheme not found")

    db.delete(scheme)
    db.commit()

    return SchemeDeleteResponse(
        message="Scheme Deleted Successfully",
        status=status.HTTP_200_OK
    )


@scheme_router.put("/{scheme_id}", response_model=SchemeSuccessResponse)
async def update_scheme(scheme_id: str, scheme_data: SchemeCreate,
                        db: Session = Depends(get_db),
                        current_user: dict = Depends(get_current_user)):
    ensure_admin_or_employee(current_user)

    scheme = SchemeQueries.get_by_id(db, scheme_id)
    if not scheme:
        raise SchemeNotFound(status_code=404, detail="Scheme not found")

    scheme.name = scheme_data.name
    scheme.description = scheme_data.description
    scheme.plan_id = scheme_data.plan_id
    db.commit()
    db.refresh(scheme)

    return SchemeSuccessResponse(
        message="Scheme Updated Successfully",
        payload=SchemeRead.model_validate(scheme),
        status=status.HTTP_200_OK
    )
