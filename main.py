from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from celery import Celery

DATABASE_URL = "mysql+asyncmy://admin:Iltdfbigmaar#1@localhost:3306/reviews_db"
REDIS_URL = "redis://localhost:6379/0"

app = FastAPI()

# SQLAlchemy setup
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Celery setup
celery_app = Celery(
    "tasks",
    broker="redis://localhost:3306/0",  # Redis URL
    backend="redis://localhost:3306/0"  # Redis URL for results
)

async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()

@app.get("/reviews/trends")
async def get_review_trends():
    async with async_session() as session:
        # Write query logic to get top 5 categories with descending average stars
        pass
    # Trigger Celery task to log access
    celery.send_task("log_access", args=["GET /reviews/trends"])
    return {"message": "Trends data"}

@app.get("/reviews/")
async def get_reviews_by_category(category_id: int):
    async with async_session() as session:
        # Write query logic to fetch paginated reviews
        pass
    # Trigger Celery task to log access
    celery.send_task("log_access", args=[f"GET /reviews/?category_id={category_id}"])
    return {"message": "Reviews data"}
