
import random
from math import floor

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from app.auth.oauth2 import get_current_user
from app.db.session import get_db
from app.models import Scheme, Plan
from app.models.policy_model import Policy
from app.models.transaction_model import Transaction
from app.models.commission_model import Commission
from app.utils.transaction_enum import TransactionStatus, TransactionType


payment_router = APIRouter(
    prefix="/payment",
    tags=["Payment"]
)


def calculate_commission_percentage(policy_id: str,
                                    db: Session = Depends(get_db)) -> float:
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise ValueError("Policy not found")

    scheme = db.query(Scheme).filter(Scheme.id == policy.scheme_id).first()
    if not scheme:
        raise ValueError("Scheme not found")

    plan = db.query(Plan).filter(Plan.id == scheme.plan_id).first()
    if not plan:
        raise ValueError("Plan not found")

    commission_floor = plan.commission_floor
    commission_ceil = plan.commission_ceil

    policy_count = db.query(Policy).filter(
        (Policy.scheme_id == policy.scheme_id) & (
                    Policy.agent_id == policy.agent_id)
    ).count()

    commission_percentage = floor(policy_count / 30) * 2 + commission_floor
    commission_percentage = min(commission_percentage, commission_ceil)

    return commission_percentage


@payment_router.post('/{policy_id}')
async def pay_policy(policy_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    status_choice = random.choice([TransactionStatus.success, TransactionStatus.failed])


    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")


    transaction = Transaction(
        policy_id= policy.id,
        type=TransactionType.purchase,
        status=status_choice
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)


    if transaction.status == TransactionStatus.success:
        try:
            commission_percentage = calculate_commission_percentage(policy.id, db)
            commission_amount = (policy.premium_amount * commission_percentage) / 100

            commission = Commission(
                txn_id=transaction.transaction_id,
                commission_amt=commission_amount
            )
            db.add(commission)
            db.commit()
        except Exception as e:
            print(f"Commission generation failed: {e}")

        return RedirectResponse(
            url=f"/transactions/{transaction.transaction_id}",
            status_code=status.HTTP_303_SEE_OTHER
        )


    return RedirectResponse(
        url=f"/transactions/{transaction.transaction_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )


