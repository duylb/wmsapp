from pydantic import BaseModel
from datetime import datetime
from typing import List


class PayrollGenerateRequest(BaseModel):
    month: int
    year: int


class PayrollRecordResponse(BaseModel):
    staff_id: int
    total_hours: float
    salary_amount: float


class PayrollPeriodResponse(BaseModel):
    id: int
    month: int
    year: int
    is_locked: bool
    generated_at: datetime
    records: List[PayrollRecordResponse]

    class Config:
        from_attributes = True