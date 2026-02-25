from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.staff import Staff


def get_all_staff(db: Session, company_id: int):
    return db.query(Staff).filter(
        Staff.company_id == company_id,
        Staff.is_active == True
    ).all()


def create_staff(db: Session, company_id: int, data):
    existing = None
    if data.email:
        existing = db.query(Staff).filter(
            Staff.company_id == company_id,
            Staff.email == data.email
        ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Staff already exists")

    staff = Staff(
        company_id=company_id,
        full_name=data.full_name,
        position=data.position,
        phone=data.phone,
        email=data.email,
        address=data.address,
        salary_type=data.salary_type,
        hourly_rate=data.hourly_rate,
        package_salary=data.package_salary,
    )

    db.add(staff)
    db.commit()
    db.refresh(staff)

    return staff


def update_staff(db: Session, company_id: int, staff_id: int, data):
    staff = db.query(Staff).filter(
        Staff.id == staff_id,
        Staff.company_id == company_id
    ).first()

    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(staff, key, value)

    db.commit()
    db.refresh(staff)

    return staff


def deactivate_staff(db: Session, company_id: int, staff_id: int):
    staff = db.query(Staff).filter(
        Staff.id == staff_id,
        Staff.company_id == company_id
    ).first()

    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    staff.is_active = False
    db.commit()