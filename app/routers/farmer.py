from fastapi import APIRouter, Depends, HTTPException
from app.routers.auth import get_current_user_from_token
from app.db import db

router = APIRouter()
farmers_collection = db["farmers"]


@router.post("/create")
async def create_farmer_profile(profile: dict, user=Depends(get_current_user_from_token)):
    """Create farmer profile for logged-in user"""
    existing = await farmers_collection.find_one({"user_id": user["_id"]})
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")

    profile["user_id"] = user["_id"]
    result = await farmers_collection.insert_one(profile)
    return {"message": "Farmer profile created", "id": str(result.inserted_id)}


@router.get("/me")
async def get_my_profile(user=Depends(get_current_user_from_token)):
    """Fetch logged-in farmer profile"""
    profile = await farmers_collection.find_one({"user_id": user["_id"]})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    profile["_id"] = str(profile["_id"])
    return profile


@router.put("/update")
async def update_farmer_profile(update_data: dict, user=Depends(get_current_user_from_token)):
    """Update logged-in farmer profile"""
    result = await farmers_collection.update_one(
        {"user_id": user["_id"]}, {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Profile not found or no changes made")
    return {"message": "Profile updated successfully"}


@router.delete("/delete")
async def delete_farmer_profile(user=Depends(get_current_user_from_token)):
    """Delete logged-in farmer profile"""
    result = await farmers_collection.delete_one({"user_id": user["_id"]})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile deleted successfully"}
