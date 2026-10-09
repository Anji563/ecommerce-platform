import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Read DATABASE_URL from Render environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Render uses 'postgres://', but SQLAlchemy 2.0 requires 'postgresql://'
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Default fallback to local docker 'db' only if DATABASE_URL is not set
if not DATABASE_URL:
    DATABASE_URL = "postgresql://ecommerce_user:password@db:5432/ecommerce"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()