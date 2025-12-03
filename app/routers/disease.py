from fastapi import APIRouter, UploadFile

router = APIRouter()

@router.post("/detect")
async def detect_disease(file: UploadFile):
    """
    Mock plant disease detection (replace with ML image model later).
    """
    return {"disease": "Leaf Rust", "treatment": "Use fungicide XYZ"}
