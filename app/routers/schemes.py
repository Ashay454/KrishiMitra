from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, HttpUrl
from typing import List, Dict
from app.db import db
from app.services.crud import find_documents
from app.services.schemes_sync import sync_schemes

router = APIRouter(
    prefix="/schemes",
    tags=["Government Schemes"],
    responses={404: {"description": "Not found"}},
)

SCHEMES_COLLECTION = db["gov_schemes"]


class SchemeModel(BaseModel):
    title: str
    description: str
    department: str
    eligibility: str
    link: HttpUrl

    class Config:
        schema_extra = {
            "example": {
                "title": "Pradhan Mantri Mudra Yojana",
                "description": "Provides loans up to 10 lakhs to small/micro enterprises.",
                "department": "Ministry of Finance",
                "eligibility": "Non-corporate small businesses",
                "link": "https://www.mudra.org.in/"
            }
        }

@router.get(
    "/all",
    summary="Get All Government Schemes",
    description="Fetches a list of government schemes stored in the database. Returns up to 100 entries.",
    response_model=Dict[str, List[SchemeModel]]
)
async def get_all_schemes():
    schemes = await find_documents(SCHEMES_COLLECTION, {}, limit=100)
    return {"schemes": schemes}


@router.post(
    "/add",
    summary="Manually Add a Government Scheme",
    description="Allows manual entry of a government scheme with all required fields via Swagger UI.",
    response_model=Dict[str, str]
)
async def add_scheme_manually(scheme: SchemeModel = Body(...)):
    await SCHEMES_COLLECTION.insert_one(scheme.dict())
    return {"message": "Scheme added successfully"}


@router.post(
    "/sync",
    summary="Sync Schemes from Government Portal",
    description="Manually triggers syncing of the latest schemes from the government portal (mocked for demo).",
    response_description="Sync status and details"
)
async def sync_government_schemes():
    try:
        result = await sync_schemes()
        return {"status": "success", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/demo/populate",
    summary="Populate Dummy Schemes (Demo Only)",
    description="Inserts a few dummy government schemes into the database for demonstration."
)
async def populate_dummy_schemes():
    demo_data = [
        {
            "title": "Pradhan Mantri Awas Yojana",
            "description": "Affordable housing for all.",
            "department": "Ministry of Housing and Urban Affairs",
            "eligibility": "Low income group",
            "link": "https://pmaymis.gov.in/"
        },
        {
            "title": "Startup India",
            "description": "Support and funding for startups.",
            "department": "Ministry of Commerce",
            "eligibility": "Recognized startups",
            "link": "https://www.startupindia.gov.in/"
        },
        {
            "title": "Digital India",
            "description": "Digital infrastructure for all citizens.",
            "department": "Ministry of Electronics and IT",
            "eligibility": "All Indian citizens",
            "link": "https://www.digitalindia.gov.in/"
        }
    ]
    await SCHEMES_COLLECTION.insert_many(demo_data)
    return {"message": "Dummy schemes inserted successfully"}
