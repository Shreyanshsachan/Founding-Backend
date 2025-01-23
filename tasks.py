from celery import Celery
import openai

celery = Celery("tasks", broker="redis://localhost:6379/0")

@celery.task
def log_access(log_text: str):
    # Save the log to the AccessLog table
    async with async_session() as session:
        session.add(AccessLog(text=log_text))
        await session.commit()


@celery.task
def fetch_tone_and_sentiment(text: str, stars: int):
    """
    Fetch tone and sentiment using an LLM (e.g., OpenAI GPT).
    """
    openai.api_key = "openai_api_key" # I have generated my key from Open AI Dashboard.
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Analyze the tone and sentiment of this review:\nText: {text}\nStars: {stars}\n",
        max_tokens=50
    )
    output = response.choices[0].text.strip().split("\n")
    tone, sentiment = output[0], output[1]
    return tone, sentiment
