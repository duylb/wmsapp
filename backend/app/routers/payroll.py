from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.schemas.payroll import (
    PayrollGenerateRequest,
    PayrollPeriodResponse,
)
from app.services.payroll_service import generate_monthly_payroll
from app.models.payroll import PayrollPeriod, PayrollRecord
from app.dependencies.auth import get_current_user

router = APIRouter()


@router.post("/generate", response_model=PayrollPeriodResponse)
def generate_payroll(
    data: PayrollGenerateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    period = generate_monthly_payroll(
        db=db,
        company_id=current_user.company_id,
        month=data.month,
        year=data.year,
    )

    records = db.query(PayrollRecord).filter(
        PayrollRecord.payroll_period_id == period.id
    ).all()

    return {
        "id": period.id,
        "month": period.month,
        "year": period.year,
        "is_locked": period.is_locked,
        "generated_at": period.generated_at,
        "records": records,
    }


@router.get("/", response_model=List[PayrollPeriodResponse])
def list_payroll_periods(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    periods = db.query(PayrollPeriod).filter(
        PayrollPeriod.company_id == current_user.company_id
    ).all()

    return periods