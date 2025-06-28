from datetime import datetime, timedelta, timezone

from app.config.logger_config import func_logger
from app.db.session import SessionLocal
from app.models.customer_model import Customer
from app.models.policy_model import Policy
from app.tasks.celery_worker import celery_app
from app.utils.send_email import send_email


@celery_app.task
def send_expiry_reminder():
    func_logger.info("Policy expiry reminder task started")
    db = SessionLocal()
    try:
        today = datetime.now(timezone.utc).date()
        expiry_date = today + timedelta(days=7)

        policies = db.query(Policy).filter(Policy.expiry_date == expiry_date).all()

        for policy in policies:
            customer = (
                db.query(Customer).filter(Customer.id == policy.customer_id).first()
            )
            if customer:
                send_email(
                    to=customer.email,
                    subject="Policy Expiry Reminder",
                    body=f"Dear {customer.name}, your policy '{policy.name}' will expire on {policy.expiry_date.date()}. Please renew it soon.",
                )
                func_logger.info(f"Sent reminder to {customer.email}")

    except Exception as e:
        func_logger.error(f"Error sending reminders: {e}")
    finally:
        db.close()
