from fastapi import APIRouter, File, UploadFile
import shutil
from services.gemini_service import analyze_image, analyze_video

router = APIRouter()

@router.post("/analyze_image/")
async def upload_image(file: UploadFile = File(...)):
    """Upload an image and analyze it for disaster detection."""
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    response = analyze_image(file_path)
    return {"analysis": response}

@router.post("/analyze_video/")
async def upload_video(file: UploadFile = File(...)):
    """Upload a video and analyze it for disaster detection."""
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    response = analyze_video(file_path)
    return {"analysis": response}