from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.company import Company


def get_company_by_id(db: Session, company_id: int):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company