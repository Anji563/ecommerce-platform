from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional

from app.database import engine, Base, get_db
from app.models import Product
from app.routers import webhooks

# Automatically create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce Async Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhooks.router)

@app.get("/api/v1/products")
def get_products(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if search:
        query = query.filter(Product.title.ilike(f"%{search}%"))
    if category:
        query = query.filter(Product.category == category)
    return query.all()