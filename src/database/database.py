from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine, Column, INT
from src.types_.settings import DATABASE_URL


class Base(DeclarativeBase):
    engine = create_engine(DATABASE_URL)
    session = sessionmaker(bind=engine)

    id = Column(INT, primary_key=True)

