from sqlalchemy import Column, Integer, String, LargeBinary
from db import Base, engine


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    embedding = Column(LargeBinary, nullable=False) 


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Table 'destinations' created (or already exists).")