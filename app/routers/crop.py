from fastapi import APIRouter

router = APIRouter()

@router.post("/recommend")
async def recommend_crop(soil_type: str, rainfall: float, season: str):
    """
    Mock AI Crop Recommendation (replace with ML model later).
    """
    if soil_type == "loamy" and season == "kharif":
        return {"recommended_crop": "Rice"}
    elif soil_type == "clay" and season == "rabi":
        return {"recommended_crop": "Wheat"}
    else:
        return {"recommended_crop": "Maize"}
