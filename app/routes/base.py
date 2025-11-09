# app/routes/base.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.database import SessionLocal
from app.models import Purchase

router = APIRouter()

# --- схема входных данных ---
class PurchaseIn(BaseModel):
    purchase_number: str
    law: str | None = None
    customer: str | None = None
    subject: str | None = None
    amount: float | None = None
    date_start: str | None = None
    date_end: str | None = None
    status: str | None = None
    region: str | None = None
    url: str | None = None


# --- зависимость для БД ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def root():
    return {"message": "Сервер работает! 🚀"}


@router.post("/upload")
def upload_purchases(purchases: List[PurchaseIn], db: Session = Depends(get_db)):
    inserted = 0
    for p in purchases:
        # Проверяем, нет ли дублей по purchase_number
        existing = db.query(Purchase).filter(Purchase.purchase_number == p.purchase_number).first()
        if not existing:
            new_p = Purchase(**p.dict())
            db.add(new_p)
            inserted += 1
    db.commit()
    return {"inserted": inserted}
