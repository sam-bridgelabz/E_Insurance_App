import random
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.auth.oauth2 import get_current_user
from app.db.session import get_db
from app.models.transaction_model import Transaction
from app.schemas.transaction_schema import TransactionCreate, TransactionResponse
from app.services.email_invoice_service import InvoiceService
from app.utils.transaction_enum import TransactionStatus

transaction_router = APIRouter(prefix="/transactions", tags=["Transaction"])

@transaction_router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    transaction_data = transaction.model_dump()
    
    status_choices = [
        TransactionStatus.success,
        TransactionStatus.failed,
        TransactionStatus.pending 
    ]
    transaction_data["status"] = random.choice(status_choices)
    
    new_transaction = Transaction(**transaction_data)
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    
    if new_transaction.status == TransactionStatus.success:
        try:
            InvoiceService.send_invoice_email(db, new_transaction)
        except Exception as e:
            print(f"Email sending failed: {e}")
    
    return new_transaction

@transaction_router.get("/", response_model=List[TransactionResponse])
def get_all_transactions(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(Transaction).all()

@transaction_router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction_by_id(transaction_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction
