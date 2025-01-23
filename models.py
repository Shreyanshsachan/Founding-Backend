from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ReviewHistory(Base):
    """
    Represents the historical versions of reviews. Each `review_id` can have 
    multiple entries (versions), identified by the `created_at` timestamp.
    """
    __tablename__ = 'review_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=True)
    stars = Column(Integer, nullable=False)  # Rating between 1 and 10
    review_id = Column(String(255), nullable=False)  # Unique identifier for reviews
    tone = Column(String(255), nullable=True)  # Analysis of tone
    sentiment = Column(String(255), nullable=True)  # Positive, Neutral, Negative sentiment
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)  # Linked to Category
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Category(Base):
    """
    Represents a category for reviews, e.g., Electronics, Books, etc.
    """
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)  # Category name
    description = Column(Text, nullable=False)  # Description of the category


class AccessLog(Base):
    """
    Logs all API accesses asynchronously for auditing purposes.
    """
    __tablename__ = 'access_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)  # Details of the access log
