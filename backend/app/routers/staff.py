from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.schemas.staff import StaffCreate, StaffUpdate, StaffResponse
from app.services.staff_service import (
    get_all_staff,
    create_staff,
    update_staff,
    deactivate_staff,
)
from app.dependencies.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[StaffResponse])
def list_staff(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_all_staff(db, current_user.company_id)


@router.post("/", response_model=StaffResponse)
def add_staff(
    data: StaffCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_staff(db, current_user.company_id, data)


@router.put("/{staff_id}", response_model=StaffResponse)
def edit_staff(
    staff_id: int,
    data: StaffUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return update_staff(db, current_user.company_id, staff_id, data)


@router.delete("/{staff_id}")
def delete_staff(
    staff_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deactivate_staff(db, current_user.company_id, staff_id)
    return {"message": "Staff deactivated"}