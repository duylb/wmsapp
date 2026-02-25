from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.company import Company
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token


def register_company(db: Session, company_name: str, company_slug: str,
                     full_name: str, email: str, password: str):

    existing = db.query(Company).filter(Company.slug == company_slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company slug already exists")

    company = Company(name=company_name, slug=company_slug)
    db.add(company)
    db.commit()
    db.refresh(company)

    user = User(
        company_id=company.id,
        full_name=full_name,
        email=email,
        password_hash=hash_password(password),
        role="owner",
    )

    db.add(user)
    db.commit()

    token = create_access_token({
        "user_id": user.id,
        "company_id": company.id,
        "role": user.role,
    })

    return token


def login_user(db: Session, email: str, password: str):

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token({
        "user_id": user.id,
        "company_id": user.company_id,
        "role": user.role,
    })

    return token