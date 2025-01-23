from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ReviewHistory(Base):
    __tablename__ = 'review_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=True)
    stars = Column(Integer, nullable=False)
    review_id = Column(String(255), nullable=False)
    tone = Column(String(255), nullable=True)
    sentiment = Column(String(255), nullable=True)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=False)

class AccessLog(Base):
    __tablename__ = 'access_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
