from main import Celery
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+asyncmy://root:password123@localhost:3306/reviews_db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

from celery import Celery

# Define the Celery app
celery_app = Celery(
    "tasks",
    broker="redis://localhost:3306/0",  # Redis URL for broker
    backend="redis://localhost:3306/0"  # Redis URL for results
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Example task
@celery_app.task
def add(x, y):
    return x + y
