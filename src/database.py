import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_new_review(db: Session, user_name: str, text: str, star: int, is_buyer: int = 0, is_expert: int = 0):
    new_review = Reviews(
        user_name=user_name,
        text=text,
        star=star,
        is_buyer=is_buyer,
        is_expert=is_expert
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

Base.metadata.create_all(bind=engine)
