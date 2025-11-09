# app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional

class PurchaseIn(BaseModel):
    purchase_number: str = Field(..., example="ZAK-2025-0001")
    law: Optional[str] = Field(None, example="44-ФЗ")
    customer: Optional[str] = Field(None, example="ООО Ромашка")
    subject: Optional[str] = Field(None, example="Поставка бумаги")
    amount: Optional[float] = Field(None, example=50000.0)
    date_start: Optional[str] = Field(None, example="2025-11-01")
    date_end: Optional[str] = Field(None, example="2025-11-10")
    status: Optional[str] = Field(None, example="Активна")
    region: Optional[str] = Field(None, example="Московская обл.")
    url: Optional[str] = Field(None, example="https://zakupki.gov.ru/...")

class UploadResult(BaseModel):
    inserted: int
