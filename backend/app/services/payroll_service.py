from sqlalchemy.orm import Session
from sqlalchemy import extract
from fastapi import HTTPException

from app.models.staff import Staff
from app.models.shift import Shift
from app.models.roster import Roster
from app.models.payroll import PayrollPeriod, PayrollRecord


def generate_monthly_payroll(db: Session, company_id: int, month: int, year: int):

    existing_period = db.query(PayrollPeriod).filter(
        PayrollPeriod.company_id == company_id,
        PayrollPeriod.month == month,
        PayrollPeriod.year == year
    ).first()

    if existing_period:
        raise HTTPException(status_code=400, detail="Payroll already generated")

    period = PayrollPeriod(
        company_id=company_id,
        month=month,
        year=year
    )
    db.add(period)
    db.commit()
    db.refresh(period)

    staff_list = db.query(Staff).filter(
        Staff.company_id == company_id,
        Staff.is_active == True
    ).all()

    for staff in staff_list:
        entries = db.query(Roster).filter(
            Roster.company_id == company_id,
            Roster.staff_id == staff.id,
            extract("month", Roster.date) == month,
            extract("year", Roster.date) == year
        ).all()

        total_hours = 0

        for entry in entries:
            if entry.morning_shift_id:
                shift = db.query(Shift).filter(
                    Shift.id == entry.morning_shift_id
                ).first()
                total_hours += float(shift.duration_hours)

            if entry.afternoon_shift_id:
                shift = db.query(Shift).filter(
                    Shift.id == entry.afternoon_shift_id
                ).first()
                total_hours += float(shift.duration_hours)

        if staff.salary_type == "hourly":
            salary = total_hours * float(staff.hourly_rate or 0)
        else:
            salary = float(staff.package_salary or 0)

        record = PayrollRecord(
            company_id=company_id,
            payroll_period_id=period.id,
            staff_id=staff.id,
            total_hours=total_hours,
            salary_amount=salary
        )
        db.add(record)

    db.commit()

    return period