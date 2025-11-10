# app/main.py
from fastapi import FastAPI
from app import models, database
from app.routes import base, purchases

# Создание таблиц при старте (Day 2)
models.Base.metadata.create_all(bind=database.engine)

# Инициализация FastAPI
app = FastAPI(title="Zakupki Parser API")

# Подключение роутеров
app.include_router(base.router)
app.include_router(purchases.router)

# Корневой эндпоинт
@app.get("/")
def root():
    return {"message": "Сервер работает! 🚀"}
