from fastapi import APIRouter, Depends, HTTPException, Body, Path
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

from app.db import db
from app.routers.auth import get_current_user_from_token
from app.services.crud import insert_document, find_documents

router = APIRouter()
community_collection = db["community_posts"]

def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, list):
        return [convert_objectid(o) for o in obj]
    if isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}
    return obj


class CommunityPost(BaseModel):
    title: str
    content: str

    class Config:
        schema_extra = {
            "example": {
                "title": "Need advice on pest control",
                "content": "My tomato crop is being affected by whiteflies. Any organic solutions?"
            }
        }

class CommunityReply(BaseModel):
    message: str

    class Config:
        schema_extra = {
            "example": {
                "message": "Try neem oil spray. It worked for me last season!"
            }
        }


@router.post("/post", summary="Create Post", description="Farmer creates a community post")
async def create_post(
    data: CommunityPost,
    user: dict = Depends(get_current_user_from_token)
):
    
    post = {
        "user_id": str(user["_id"]),
        "name": user.get("name"),
        "title": data.title,
        "content": data.content,
        "created_at": datetime.utcnow(),
        "replies": []
    }
    post_id = await insert_document(community_collection, post)
    return {"message": "Post created", "id": str(post_id)}

@router.get("/all", summary="Get All Posts", description="Get the 100 most recent community posts")
async def get_posts():
    """Get all community posts"""
    posts = await find_documents(community_collection, {}, limit=100)
    return [convert_objectid(post) for post in posts]

@router.post("/reply/{post_id}", summary="Reply to a Post", description="Authenticated user replies to a community post")
async def reply_post(
    post_id: str = Path(..., description="ID of the post to reply to"),
    reply: CommunityReply = Body(...),
    user: dict = Depends(get_current_user_from_token)
):
    
    try:
        post_obj_id = ObjectId(post_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid post ID")

    post = await community_collection.find_one({"_id": post_obj_id})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_reply = {
        "user_id": str(user["_id"]),
        "name": user.get("name"),
        "message": reply.message,
        "created_at": datetime.utcnow()
    }

    await community_collection.update_one(
        {"_id": post_obj_id},
        {"$push": {"replies": new_reply}}
    )
    return {"message": "Reply added"}
