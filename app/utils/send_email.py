import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config.load_config import smtp_settings
from app.config.logger_config import func_logger


def send_email(to: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg["From"] = smtp_settings.SMTP_USERNAME
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_settings.SMTP_SERVER, smtp_settings.SMTP_PORT) as server:
        server.starttls()
        server.login(smtp_settings.SMTP_USERNAME, smtp_settings.SMTP_PASSWORD)
        server.send_message(msg)
        func_logger.info(f"mail delivered to {to}")
