from sqlalchemy import create_engine, MetaData

DATABASE_URL = "postgresql://travel_user:123456@localhost:5432/travel_rec_db"

engine = create_engine(DATABASE_URL)
metadata = MetaData()