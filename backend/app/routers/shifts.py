from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.schemas.shift import ShiftResponse, ShiftUpdate
from app.services.shift_service import (
    get_all_shifts,
    update_shift_duration,
)
from app.dependencies.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[ShiftResponse])
def list_shifts(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_all_shifts(db, current_user.company_id)


@router.put("/{shift_id}", response_model=ShiftResponse)
def update_shift(
    shift_id: int,
    data: ShiftUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return update_shift_duration(
        db,
        current_user.company_id,
        shift_id,
        data.duration_hours
    )