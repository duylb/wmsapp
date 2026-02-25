from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.shift import Shift


DEFAULT_SHIFTS = [
    "S1","S2","S3","S4","S5","S6",
    "B1","B2","B3","B4","B5","B6"
]


def init_default_shifts(db: Session, company_id: int):
    existing = db.query(Shift).filter(
        Shift.company_id == company_id
    ).count()

    if existing > 0:
        return

    for name in DEFAULT_SHIFTS:
        shift = Shift(
            company_id=company_id,
            name=name,
            duration_hours=8
        )
        db.add(shift)

    db.commit()


def get_all_shifts(db: Session, company_id: int):
    return db.query(Shift).filter(
        Shift.company_id == company_id
    ).all()


def update_shift_duration(db: Session, company_id: int, shift_id: int, duration: float):
    shift = db.query(Shift).filter(
        Shift.id == shift_id,
        Shift.company_id == company_id
    ).first()

    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")

    shift.duration_hours = duration
    db.commit()
    db.refresh(shift)

    return shift