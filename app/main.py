# app/main.py
from fastapi import FastAPI
from app import models, database
from app.routes.purchases import router as purchases_router
from app.routes.base import router as base_router

# Создание таблиц при старте (Day 2)
models.Base.metadata.create_all(bind=database.engine)

# Инициализация FastAPI
app = FastAPI(title="Zakupki Parser API")

# Подключение роутеров
app.include_router(base_router)
app.include_router(purchases_router)

# Корневой эндпоинт
@app.get("/")
def root():
    return {"message": "Сервер работает! 🚀"}
