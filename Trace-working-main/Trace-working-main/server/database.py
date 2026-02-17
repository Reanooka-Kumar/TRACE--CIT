from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")   # ← FIXED
DB_NAME = os.getenv("DB_NAME", "trace_db")

if not DB_PASSWORD:
    raise RuntimeError("DB_PASSWORD not set in .env file")

encoded_user = urllib.parse.quote_plus(DB_USER)
encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{encoded_user}:{encoded_password}@{DB_HOST}/{DB_NAME}"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=3600,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
