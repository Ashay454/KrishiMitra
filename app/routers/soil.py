from fastapi import APIRouter, HTTPException, Query
import os
import httpx
from dotenv import load_dotenv
import traceback

router = APIRouter()

load_dotenv()
SOILGRIDS_URL = os.getenv("SOILGRIDS_BASE_URL", "https://rest.isric.org/soilgrids/v2.0/properties/query")


@router.get("/soil")
async def get_soil_data(lat: float = Query(..., description="Latitude"),
                        lon: float = Query(..., description="Longitude")):
    """
    Get all soil properties and their depth-wise mean values for given latitude and longitude.
    Example: /soil?lat=26.85&lon=80.95
    """
    try:
        params = {"lat": lat, "lon": lon}
        async with httpx.AsyncClient() as client:
            resp = await client.get(SOILGRIDS_URL, params=params, timeout=30.0)

        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=f"SoilGrids API error: {resp.text}")

        data = resp.json()
        layers = data.get("properties", {}).get("layers", [])
        if not layers:
            raise HTTPException(status_code=500, detail="No soil layers found in SoilGrids response")

        result = {}

        for layer in layers:
            property_name = layer.get("name")
            depths_data = []
            for depth_info in layer.get("depths", []):
                depth_range = depth_info.get("depth_range")
                mean_val = depth_info.get("values", {}).get("mean")
                if mean_val is not None:
                    depths_data.append({
                        "depth_range": depth_range,
                        "mean": mean_val
                    })
            result[property_name] = depths_data

        return {
            "latitude": lat,
            "longitude": lon,
            "soil_properties": result
        }

    except httpx.ReadTimeout:
        raise HTTPException(status_code=504, detail="Request to SoilGrids timed out. Please try again later.")
    except HTTPException:
        raise
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Internal error: {str(e) or 'Unknown error'}\nTraceback:\n{tb}"
        )
