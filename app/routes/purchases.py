# app/routes/purchases.py
import io
import csv
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import pandas as pd
from .. import models, schemas, database

router = APIRouter(prefix="/purchases", tags=["Purchases"])

# Dependency для подключения к БД
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🟢 CREATE: добавить одну или несколько закупок
@router.post("/upload")
def upload_purchases(purchases: list[schemas.PurchaseCreate], db: Session = Depends(get_db)):
    inserted = 0
    for purchase_data in purchases:
        # Проверяем дубликаты по purchase_number
        existing = db.query(models.Purchase).filter(models.Purchase.purchase_number == purchase_data.purchase_number).first()
        if existing:
            continue  # пропускаем, если уже есть

        new_purchase = models.Purchase(**purchase_data.dict())
        db.add(new_purchase)
        inserted += 1

    db.commit()
    return {"inserted": inserted}

# 🔵 READ: получить все закупки
@router.get("/", response_model=list[schemas.PurchaseResponse])
def get_purchases(db: Session = Depends(get_db)):
    purchases = db.query(models.Purchase).all()
    return purchases

# 🟡 READ: получить одну закупку по ID
@router.get("/{purchase_id}", response_model=schemas.PurchaseResponse)
def get_purchase(purchase_id: int, db: Session = Depends(get_db)):
    purchase = db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Закупка не найдена")
    return purchase

# 🟠 UPDATE: обновить закупку
@router.put("/{purchase_id}")
def update_purchase(purchase_id: int, updated: schemas.PurchaseCreate, db: Session = Depends(get_db)):
    purchase = db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Закупка не найдена")

    for key, value in updated.dict().items():
        setattr(purchase, key, value)
    db.commit()
    db.refresh(purchase)
    return {"updated": purchase_id}

# 🔴 DELETE: удалить закупку
@router.delete("/{purchase_id}")
def delete_purchase(purchase_id: int, db: Session = Depends(get_db)):
    purchase = db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Закупка не найдена")
    db.delete(purchase)
    db.commit()
    return {"deleted": purchase_id}

# --- Экспорт CSV ---
@router.get("/export/csv", response_class=StreamingResponse, tags=["Purchases"])
def export_csv(db: Session = Depends(get_db)):
    ...

# --- Экспорт Excel ---
@router.get("/export/excel", response_class=StreamingResponse, tags=["Purchases"])
def export_excel(db: Session = Depends(get_db)):
    ...