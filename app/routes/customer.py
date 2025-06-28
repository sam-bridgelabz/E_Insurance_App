from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.oauth2 import get_current_user
from app.db.session import get_db
from app.exceptions.orm import CustomerNotFound, EmailAlreadyExists, UnauthorizedAccess
from app.models.customer_model import Customer
from app.schemas.customer_schema import CustomerCreate, CustomerResponse, CustomerUpdate
from app.utils.hash_password import Hash

customer_router = APIRouter(prefix="/customers", tags=["Customer"])


def ensure_admin_or_agent(current_user: dict):
    if current_user["role"] not in ["agent", "admin"]:
        raise UnauthorizedAccess(
            status_code=403, detail="Access denied: Only admin or agent allowed"
        )


@customer_router.post(
    "/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    ensure_admin_or_agent(current_user)
    if db.query(Customer).filter(Customer.email == customer.email).first():
        raise EmailAlreadyExists(detail="Customer with this email already exists")

    customer_data = customer.model_dump()
    customer_data["password"] = Hash.get_hash_password(customer.password)
    customer_data["agent_id"] = current_user["user"].id

    new_customer = Customer(**customer_data)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


@customer_router.get("/", response_model=List[CustomerResponse])
def get_all_customers(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return db.query(Customer).all()


@customer_router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise CustomerNotFound()
    return customer


@customer_router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    ensure_admin_or_agent(current_user)
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise CustomerNotFound()
    if current_user["role"] != "admin" and customer.agent_id != current_user["user"].id:
        raise UnauthorizedAccess(detail="You can only delete your own customers")
    db.delete(customer)
    db.commit()
    return


@customer_router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: str,
    updated_data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    ensure_admin_or_agent(current_user)
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise CustomerNotFound()

    if current_user["role"] != "admin" and customer.agent_id != current_user["user"].id:
        raise UnauthorizedAccess(detail="You can only update your own customers")

    update_data = updated_data.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = Hash.get_hash_password(update_data["password"])

    for key, value in update_data.items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer
