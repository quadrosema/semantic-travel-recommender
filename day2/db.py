from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace with your actual credentials if different
DATABASE_URL = "postgresql://travel_user:123456@localhost:5432/travel_rec_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_session():
    return SessionLocal()