from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.services.auth_service import register_company, login_user

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    token = register_company(
        db=db,
        company_name=data.company_name,
        company_slug=data.company_slug,
        full_name=data.full_name,
        email=data.email,
        password=data.password,
    )
    return {"access_token": token}


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    token = login_user(
        db=db,
        email=data.email,
        password=data.password,
    )
    return {"access_token": token}