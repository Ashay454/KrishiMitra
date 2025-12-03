from fastapi import APIRouter, HTTPException
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise Exception("Missing OpenWeatherMap API Key")

@router.get("/weather/{city}")
async def get_weather(city: str):
    """
    Fetch current weather for a city using OpenWeatherMap API.
    Example: /weather/London
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="City not found or API error")

    data = response.json()
    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }
