# app/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PurchaseCreate(BaseModel):
    purchase_number: str
    law: Optional[str] = None
    customer: Optional[str] = None
    subject: Optional[str] = None
    amount: Optional[float] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    status: Optional[str] = None
    region: Optional[str] = None
    url: Optional[str] = None

class PurchaseResponse(PurchaseCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
