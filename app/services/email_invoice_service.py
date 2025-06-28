from sqlalchemy.orm import Session

from app.config.logger_config import func_logger
from app.db.session import get_db
from app.models.customer_model import Customer
from app.models.policy_model import Policy
from app.models.transaction_model import Transaction
from app.utils.send_email import send_email


class InvoiceService:
    @staticmethod
    def generate_invoice_data(db: Session, transaction: Transaction) -> dict:
        policy = db.query(Policy).filter(Policy.id == transaction.policy_id).first()
        customer = db.query(Customer).filter(Customer.id == policy.customer_id).first()

        return {
            "transaction_id": transaction.transaction_id,
            "policy_name": policy.name,
            "amount": policy.premium_amount,
            "date": transaction.date.strftime("%Y-%m-%d"),
            "status": transaction.status.value,
            "customer_name": customer.name,
            "customer_email": customer.email,
        }

    @classmethod
    def send_invoice_email(cls, db: Session, transaction: Transaction):
        invoice_data = cls.generate_invoice_data(db, transaction)

        subject = f"Invoice #{invoice_data['transaction_id']}"
        body = f"""
        Dear {invoice_data['customer_name']},

        Your Transaction's Invoice Details:
        - Transaction ID: {invoice_data['transaction_id']}
        - Policy: {invoice_data['policy_name']}
        - Amount: RS. {invoice_data['amount']}
        - Date: {invoice_data['date']}
        - Status: {invoice_data['status']}
        """

        send_email(to=invoice_data["customer_email"], subject=subject, body=body)
