from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.database.session import get_db
from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffUpdate, StaffResponse
from app.core.tenant import get_current_company_id
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/staff", tags=["Staff"])


@router.get("/", response_model=list[StaffResponse])
def list_staff(
    db: Session = Depends(get_db),
    company_id: UUID = Depends(get_current_company_id),
):
    return (
        db.query(Staff)
        .filter(
            Staff.company_id == company_id,
            Staff.is_active == True,
        )
        .all()
    )


@router.post("/", response_model=StaffResponse)
def create_staff(
    payload: StaffCreate,
    db: Session = Depends(get_db),
    company_id: UUID = Depends(get_current_company_id),
):
    staff = Staff(
        **payload.dict(),
        company_id=company_id,
    )

    db.add(staff)
    db.commit()
    db.refresh(staff)

    return staff


@router.put("/{staff_id}", response_model=StaffResponse)
def update_staff(
    staff_id: UUID,
    payload: StaffUpdate,
    db: Session = Depends(get_db),
    company_id: UUID = Depends(get_current_company_id),
):
    staff = (
        db.query(Staff)
        .filter(
            Staff.id == staff_id,
            Staff.company_id == company_id,
        )
        .first()
    )

    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff not found",
        )

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(staff, key, value)

    db.commit()
    db.refresh(staff)

    return staff


@router.delete("/{staff_id}")
def deactivate_staff(
    staff_id: UUID,
    db: Session = Depends(get_db),
    company_id: UUID = Depends(get_current_company_id),
):
    staff = (
        db.query(Staff)
        .filter(
            Staff.id == staff_id,
            Staff.company_id == company_id,
        )
        .first()
    )

    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff not found",
        )

    staff.is_active = False

    db.commit()

    return {"message": "Staff deactivated successfully"}