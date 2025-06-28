from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.oauth2 import get_current_user
from app.db.session import get_db
from app.exceptions.orm import (
    ExpiryDateError,
    PolicyAlreadyExists,
    PolicyNotFound,
    UnauthorizedAccess,
    ZeroAmountError,
)
from app.models.policy_model import Policy
from app.queries.scheme import PolicyQueries
from app.schemas.policy_schema import PolicyCreate, PolicyResponse

policy_router = APIRouter(prefix="/policy", tags=["Policy"])


def ensure_admin_or_agent(current_user: dict):
    if current_user["role"] not in ["agent", "admin"]:
        raise UnauthorizedAccess(
            status_code=403, detail="Access denied: Only admin or agent allowed"
        )


@policy_router.post(
    "/", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED
)
def add_policy(
    policy: PolicyCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    ensure_admin_or_agent(current_user)
    existing = PolicyQueries.get_by_name(db, policy.name)
    if existing:
        raise PolicyAlreadyExists()

    if policy.expiry_date <= policy.start_date:
        raise ExpiryDateError()

    if policy.premium_amount <= 0:
        raise ZeroAmountError()

    policy_data = policy.model_dump()
    policy_data["agent_id"] = current_user["user"].id
    new_policy = Policy(**policy_data)

    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)
    return new_policy


@policy_router.get("/", response_model=List[PolicyResponse])
def get_all_policies(
    db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    return db.query(Policy).all()


@policy_router.get("/{policy_id}", response_model=PolicyResponse)
def get_policy(
    policy_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise PolicyNotFound()
    return policy


@policy_router.put("/{policy_id}", response_model=PolicyResponse)
def update_policy(
    policy_id: str,
    updated_data: PolicyCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    ensure_admin_or_agent(current_user)

    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise PolicyNotFound()

    if policy.agent_id != current_user["id"]:
        raise UnauthorizedAccess()

    if updated_data.premium_amount <= 0:
        raise ZeroAmountError()

    if updated_data.expiry_date <= updated_data.start_date:
        raise ExpiryDateError()

    for key, value in updated_data.model_dump().items():
        setattr(policy, key, value)
    db.commit()
    db.refresh(policy)
    return policy


@policy_router.delete("/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_policy(
    policy_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    ensure_admin_or_agent(current_user)

    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise PolicyNotFound()
    db.delete(policy)
    db.commit()
    return
