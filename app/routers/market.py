from fastapi import APIRouter, HTTPException
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

API_KEY = os.getenv("MARKET_API_KEY")
if not API_KEY:
    raise Exception("MARKET_API_KEY is not set in environment variables")


RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"

@router.get("/market-price/{crop_name}")
async def get_market_price(crop_name: str):
    url = (
        f"https://api.data.gov.in/resource/{RESOURCE_ID}"
        f"?api-key={API_KEY}"
        f"&format=json"
        f"&filters[commodity]={crop_name.lower()}"
        f"&limit=1"
        f"&offset=0"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from market API")

    data = response.json()

    records = data.get("records")
    if not records:
        return {"message": f"No price data found for '{crop_name}'"}

    crop_data = records[0]

    return {
        "crop": crop_data.get("commodity"),
        "market": crop_data.get("market"),
        "state": crop_data.get("state"),
        "price": crop_data.get("modal_price"),
        "unit": "quintal",
        "date": crop_data.get("arrival_date")
    }
