from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.database.session import get_db
from app.schemas.roster import RosterCreate, RosterUpdate, RosterResponse
from app.services.roster_service import (
    upsert_roster,
    get_roster_range,
)
from app.dependencies.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=RosterResponse)
def create_or_update_roster(
    data: RosterCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return upsert_roster(
        db=db,
        company_id=current_user.company_id,
        staff_id=data.staff_id,
        roster_date=data.date,
        morning_shift_id=data.morning_shift_id,
        afternoon_shift_id=data.afternoon_shift_id,
    )


@router.get("/", response_model=List[RosterResponse])
def get_roster(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_roster_range(
        db=db,
        company_id=current_user.company_id,
        start_date=start_date,
        end_date=end_date,
    )