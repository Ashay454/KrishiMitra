from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    weather, market, crop, disease, soil, farmer, assistant, auth,
    schemes, community
)

app = FastAPI(title="KrishiMitra", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(weather.router, prefix="/weather", tags=["Weather"])
app.include_router(market.router, prefix="/market", tags=["Market"])
app.include_router(crop.router, prefix="/crop", tags=["Crop Recommendation"])
app.include_router(disease.router, prefix="/disease", tags=["Disease Detection"])
app.include_router(soil.router, prefix="/soil", tags=["Soil Data"])
app.include_router(farmer.router, prefix="/farmer", tags=["Farmer Input"])
app.include_router(assistant.router, prefix="/assistant", tags=["AI Assistant"])
app.include_router(schemes.router, prefix="/schemes", tags=["Government Schemes"])
app.include_router(community.router, prefix="/community", tags=["Community"])


@app.get("/")
def root():
    return {"message": "KrishiMitra backend is running!"}
