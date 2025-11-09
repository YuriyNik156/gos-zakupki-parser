from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database

router = APIRouter()

@router.post("/upload")
def upload_purchases(purchases: List[schemas.PurchaseCreate], db: Session = Depends(database.get_db)):
    inserted = 0
    for purchase in purchases:
        # Проверка на дубликаты
        existing = db.query(models.Purchase).filter(models.Purchase.purchase_number == purchase.purchase_number).first()
        if not existing:
            new_purchase = models.Purchase(**purchase.dict())
            db.add(new_purchase)
            inserted += 1
    db.commit()
    return {"inserted": inserted}
