# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, crud, schemas
from .database import engine, SessionLocal, Base

# Создаём таблицы при старте (Day 2)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gos Zakupki Parser")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Сервер работает! 🚀"}

@app.post("/upload", response_model=schemas.UploadResult)
def upload(purchases: List[schemas.PurchaseIn], db: Session = Depends(get_db)):
    """
    Ожидает список объектов закупок и сохраняет их, пропуская дубликаты.
    Возвращает количество вставленных записей.
    """
    if not purchases:
        raise HTTPException(status_code=400, detail="Empty payload")
    inserted = 0
    for p in purchases:
        created = crud.create_purchase(db, p)
        if created:
            inserted += 1
    return {"inserted": inserted}
