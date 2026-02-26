import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import get_password_hash
from app.tasks.email_tasks import send_email_task


def generate_token():
    return secrets.token_urlsafe(32)


def create_email_verification(user: User, db: Session):
    token = generate_token()
    user.verification_token = token
    user.verification_token_expires = datetime.utcnow() + timedelta(hours=24)
    db.commit()

    verify_link = f"https://your-frontend.com/verify-email?token={token}"

    send_email_task.delay(
        user.email,
        "Verify your account",
        f"Click to verify your account:\n{verify_link}",
    )


def create_password_reset(user: User, db: Session):
    token = generate_token()
    user.reset_token = token
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=2)
    db.commit()

    reset_link = f"https://your-frontend.com/reset-password?token={token}"

    send_email_task.delay(
        user.email,
        "Reset your password",
        f"Click to reset your password:\n{reset_link}",
    )


def reset_password(token: str, new_password: str, db: Session):
    user = db.query(User).filter(User.reset_token == token).first()

    if not user:
        return None

    if user.reset_token_expires < datetime.utcnow():
        return None

    user.hashed_password = get_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expires = None

    db.commit()
    return user