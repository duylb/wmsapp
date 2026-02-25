from pydantic import BaseModel
from datetime import datetime


class SubscriptionResponse(BaseModel):
    id: int
    plan: str
    status: str
    current_period_end: datetime | None

    class Config:
        from_attributes = True