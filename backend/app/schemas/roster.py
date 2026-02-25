from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class RosterCreate(BaseModel):
    staff_id: int
    date: date
    morning_shift_id: Optional[int] = None
    afternoon_shift_id: Optional[int] = None


class RosterUpdate(BaseModel):
    morning_shift_id: Optional[int] = None
    afternoon_shift_id: Optional[int] = None


class RosterResponse(BaseModel):
    id: int
    staff_id: int
    date: date
    morning_shift_id: Optional[int]
    afternoon_shift_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True