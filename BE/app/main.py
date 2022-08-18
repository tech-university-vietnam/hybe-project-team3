from fastapi import FastAPI
from datetime import datetime


def get_datetime_now() -> datetime:
    # Use arrow function here to mock the builtin library
    return datetime.now()


app = FastAPI()


@app.get("/day", tags=["Dates"])
def get_day_of_week():
    """
    Get the current day of week
    """

    return {
        "day": get_datetime_now().strftime("%A")
    }
