from pydantic import BaseModel
from datetime import datetime


class CompanyCreate(BaseModel):
    name: str
    slug: str


class CompanyResponse(BaseModel):
    id: int
    name: str
    slug: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True