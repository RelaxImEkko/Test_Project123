from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.api import api_router
from app.db.session import engine, SessionLocal
from app.models import Base
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Organizations Directory API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api/v1")
