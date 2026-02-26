from sqlalchemy.orm import Session
from app.models.payroll import Payroll


def generate_payroll_for_company(db: Session, company_id: str):
    # Heavy payroll logic here
    # Calculate from roster, shifts, staff rates

    payroll = Payroll(
        company_id=company_id,
        status="generated",
    )

    db.add(payroll)
    db.commit()