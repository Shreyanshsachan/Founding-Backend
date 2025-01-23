from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func
from models import Base, ReviewHistory, Category, AccessLog
from tasks import log_access, fetch_tone_and_sentiment
from typing import List

DATABASE_URL = "mysql+asyncmy://admin:Iltdfbigmaar#1@localhost:3306/reviews_db"
REDIS_URL = "redis://localhost:6379/0"

app = FastAPI()

# SQLAlchemy setup
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


@app.get("/reviews/trends")
async def get_review_trends():
    """
    Fetches top 5 categories based on descending average stars from the latest reviews.
    """
    async with async_session() as session:
        # Query for top 5 categories based on the latest reviews
        subquery = (
            select(
                ReviewHistory.category_id,
                func.max(ReviewHistory.id).label("latest_id")
            )
            .group_by(ReviewHistory.review_id)
            .subquery()
        )

        query = (
            select(
                Category.id,
                Category.name,
                Category.description,
                func.avg(ReviewHistory.stars).label("average_star"),
                func.count(ReviewHistory.id).label("total_reviews")
            )
            .join(ReviewHistory, ReviewHistory.category_id == Category.id)
            .join(subquery, subquery.c.latest_id == ReviewHistory.id)
            .group_by(Category.id)
            .order_by(func.avg(ReviewHistory.stars).desc())
            .limit(5)
        )
        result = await session.execute(query)
        data = result.fetchall()

    # Log the access asynchronously
    log_access.delay("GET /reviews/trends")

    # Prepare the response
    trends = [
        {
            "id": row.id,
            "name": row.name,
            "description": row.description,
            "average_star": row.average_star,
            "total_reviews": row.total_reviews
        }
        for row in data
    ]
    return trends


@app.get("/reviews/")
async def get_reviews_by_category(category_id: int, page: int = Query(1, ge=1)):
    """
    Fetches reviews for a particular category in a paginated way.
    """
    PAGE_SIZE = 15
    offset = (page - 1) * PAGE_SIZE

    async with async_session() as session:
        # Subquery to find the latest review for each `review_id`
        subquery = (
            select(
                ReviewHistory.review_id,
                func.max(ReviewHistory.created_at).label("latest_date")
            )
            .filter(ReviewHistory.category_id == category_id)
            .group_by(ReviewHistory.review_id)
            .subquery()
        )

        # Main query for fetching paginated data
        query = (
            select(ReviewHistory)
            .join(subquery, (ReviewHistory.review_id == subquery.c.review_id) &
                  (ReviewHistory.created_at == subquery.c.latest_date))
            .order_by(ReviewHistory.created_at.desc())
            .offset(offset)
            .limit(PAGE_SIZE)
        )

        result = await session.execute(query)
        data = result.scalars().all()

        # Calculate tone and sentiment if missing
        for review in data:
            if not review.tone or not review.sentiment:
                tone, sentiment = fetch_tone_and_sentiment(review.text, review.stars)
                review.tone = tone
                review.sentiment = sentiment
                session.add(review)
        await session.commit()

    # Log the access asynchronously
    log_access.delay(f"GET /reviews/?category_id={category_id}")

    # Prepare response
    reviews = [
        {
            "id": review.id,
            "text": review.text,
            "stars": review.stars,
            "review_id": review.review_id,
            "created_at": review.created_at,
            "tone": review.tone,
            "sentiment": review.sentiment,
            "category_id": review.category_id,
        }
        for review in data
    ]
    return reviews

