from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import date

from app.models.roster import Roster
from app.models.shift import Shift
from app.models.staff import Staff


def upsert_roster(
    db: Session,
    company_id: int,
    staff_id: int,
    roster_date: date,
    morning_shift_id: int | None,
    afternoon_shift_id: int | None,
):
    staff = db.query(Staff).filter(
        Staff.id == staff_id,
        Staff.company_id == company_id
    ).first()

    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    roster = db.query(Roster).filter(
        Roster.company_id == company_id,
        Roster.staff_id == staff_id,
        Roster.date == roster_date
    ).first()

    if roster:
        roster.morning_shift_id = morning_shift_id
        roster.afternoon_shift_id = afternoon_shift_id
    else:
        roster = Roster(
            company_id=company_id,
            staff_id=staff_id,
            date=roster_date,
            morning_shift_id=morning_shift_id,
            afternoon_shift_id=afternoon_shift_id
        )
        db.add(roster)

    db.commit()
    db.refresh(roster)

    return roster


def get_roster_range(
    db: Session,
    company_id: int,
    start_date: date,
    end_date: date
):
    return db.query(Roster).filter(
        Roster.company_id == company_id,
        Roster.date >= start_date,
        Roster.date <= end_date
    ).all()