import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

SQL_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQL_DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in environment variables!")

engine = create_engine(SQL_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Reviews(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(100), index=True, nullable=False)
    text = Column(Text)
    star = Column(Integer)
    is_buyer = Column(Integer)
    is_expert = Column(Integer)

Base.metadata.create_all(bind=engine)
