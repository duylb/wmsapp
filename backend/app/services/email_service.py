import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = None  # set in env later
SMTP_PASSWORD = None


def send_email(to_email: str, subject: str, body: str):
    if not SMTP_USER or not SMTP_PASSWORD:
        return False

    message = MIMEMultipart()
    message["From"] = SMTP_USER
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(message)
        server.quit()
        return True
    except Exception:
        return False