from celery import Celery
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import openai

# Define Celery app
celery_app = Celery('tasks', broker='redis://localhost:6379/0')

# SQLAlchemy async setup
DATABASE_URL = "mysql+asyncmy://admin:Iltdfbigmaar#1@localhost:3306/reviews_db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Replace with your OpenAI API key
openai.api_key = "your_openai_api_key"


@celery_app.task
def log_access(log_message: str):
    """
    Log API access asynchronously
    """
    import asyncio

    async def log_to_db():
        async with async_session() as session:
            async with session.begin():
                from models import AccessLog
                access_log = AccessLog(text=log_message)
                session.add(access_log)
            await session.commit()

    asyncio.run(log_to_db())  # Use asyncio to execute the async DB operation


@celery_app.task
def fetch_tone_and_sentiment(review_text: str, stars: int):
    """
    Fetch tone and sentiment using OpenAI API asynchronously
    """
    import asyncio

    async def analyze_review():
        prompt = (
            f"Analyze the following review:\n\n{review_text}\n"
            f"Stars: {stars}\n"
            "Provide the tone and sentiment."
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        tone, sentiment = response.choices[0].message['content'].strip().split('\n')
        return tone, sentiment

    tone, sentiment = asyncio.run(analyze_review())  # Handle async logic execution
    return {"tone": tone, "sentiment": sentiment}
