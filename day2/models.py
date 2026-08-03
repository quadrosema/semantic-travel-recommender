from sqlalchemy import Table, Column, Integer, String, LargeBinary
from db import metadata, engine

destinations = Table(
    "destinations",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("country", String, nullable=False),
    Column("description", String, nullable=False),
    Column("category", String, nullable=False),
    Column("embedding", LargeBinary, nullable=False),  # stored as bytes
)

if __name__ == "__main__":
    metadata.create_all(engine)
    print("Table 'destinations' created (or already exists).")