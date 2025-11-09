# app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    purchase_number = Column(String, unique=True, index=True, nullable=False)  # номер закупки (уникальный)
    law = Column(String, nullable=True)         # 44-ФЗ / 223-ФЗ (опционально)
    customer = Column(String, nullable=True)
    subject = Column(String, nullable=True)
    amount = Column(Float, nullable=True)
    date_start = Column(String, nullable=True)  # храним как строку ISO (удобно для теста)
    date_end = Column(String, nullable=True)
    status = Column(String, nullable=True)
    region = Column(String, nullable=True)
    url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
