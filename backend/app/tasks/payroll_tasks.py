from app.core.celery_app import celery_app
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.services.payroll_service import generate_payroll_for_company


@celery_app.task
def generate_payroll_task(company_id: str):
    db: Session = SessionLocal()
    try:
        generate_payroll_for_company(db, company_id)
    finally:
        db.close()