# FastAPI & Celery Review Application

## Overview
This project is a review management application built using **FastAPI** for the API, **SQLAlchemy/Alembic** for the database, and **Celery** for background task processing. It supports:
- Retrieving top 5 review categories by average stars (`/reviews/trends`).
- Fetching paginated reviews for a specific category (`/reviews/`).
- Automatically analyzing the tone and sentiment of reviews.

##Features
1. **Top Categories API**: `/reviews/trends`
   - Returns the top 5 categories by average star ratings.
   - Uses the latest version of reviews for calculations.
   - Asynchronously logs the access in the `AccessLog` table.

2. **Category Reviews API**: `/reviews/?category_id=<id>`
   - Returns paginated reviews (15 per page) for a category.
   - Automatically analyzes missing `tone` and `sentiment`.

3. **Background Processing**: Powered by **Celery** and **Redis**.

##Procedure
   - Set up the database: alembic upgrade head
   - Start the Celery worker: celery -A tasks worker --loglevel=info
   - Run the FastAPI server: uvicorn main:app --reload

API Endpoints
/reviews/trends
   - Method: GET
   - Description: Fetches the top 5 categories by average stars.
/reviews/?category_id=<id>
   - Method: GET
   - Query Params: category_id (int), page (optional)
   - Description: Fetches paginated reviews for a given category.
