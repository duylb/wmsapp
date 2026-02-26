from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import verify_password, create_access_token
from app.services.auth_service import (
    create_email_verification,
    verify_email,
    create_password_reset,
    reset_password,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/verify-email")
def verify_email_endpoint(token: str, db: Session = Depends(get_db)):
    user = verify_email(token, db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    return {"message": "Email verified successfully"}


@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user:
        create_password_reset(user, db)
    return {"message": "If account exists, reset email sent"}


@router.post("/reset-password")
def reset_password_endpoint(
    token: str,
    new_password: str,
    db: Session = Depends(get_db),
):
    user = reset_password(token, new_password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    return {"message": "Password reset successful"}