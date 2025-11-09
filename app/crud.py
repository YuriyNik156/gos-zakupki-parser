# app/crud.py
from sqlalchemy.orm import Session
from . import models
from .schemas import PurchaseIn
from typing import Optional

def get_purchase_by_number(db: Session, number: str) -> Optional[models.Purchase]:
    return db.query(models.Purchase).filter(models.Purchase.purchase_number == number).first()

def create_purchase(db: Session, purchase: PurchaseIn) -> Optional[models.Purchase]:
    # Если уже есть — возвращаем None (дубликат)
    existing = get_purchase_by_number(db, purchase.purchase_number)
    if existing:
        return None
    db_obj = models.Purchase(
        purchase_number=purchase.purchase_number,
        law=purchase.law,
        customer=purchase.customer,
        subject=purchase.subject,
        amount=purchase.amount,
        date_start=purchase.date_start,
        date_end=purchase.date_end,
        status=purchase.status,
        region=purchase.region,
        url=purchase.url
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
