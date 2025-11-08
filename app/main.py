from fastapi import FastAPI
from .routes import base

app = FastAPI(title="Gos Zakupki Parser")

app.include_router(base.router)
