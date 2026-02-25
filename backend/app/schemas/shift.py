from pydantic import BaseModel
from datetime import datetime


class ShiftCreate(BaseModel):
    name: str
    duration_hours: float


class ShiftUpdate(BaseModel):
    duration_hours: float


class ShiftResponse(BaseModel):
    id: int
    name: str
    duration_hours: float
    created_at: datetime

    class Config:
        from_attributes = True