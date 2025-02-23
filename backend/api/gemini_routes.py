from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Header
import shutil
from services.gemini_service import analyze_image, analyze_video
from fastapi.responses import JSONResponse
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

# Rate limiting (example: 5 requests per minute)
RATE_LIMIT = 5
TIME_WINDOW = 60  # seconds
request_counts = {}

async def rate_limit(client_ip: str):
    """Rate limits the API requests."""
    if client_ip not in request_counts:
        request_counts[client_ip] = []
    
    now = time.time()
    # Remove requests older than the time window
    request_counts[client_ip] = [ts for ts in request_counts[client_ip] if now - ts < TIME_WINDOW]
    
    if len(request_counts[client_ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
    
    request_counts[client_ip].append(now)

@router.post("/analyze_image/")
async def upload_image(file: UploadFile = File(...), client_ip: str = Header(None)):
    """Upload an image and analyze it for disaster detection."""
    try:
        await rate_limit(client_ip)  # Apply rate limiting

        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        response = analyze_image(file_path)
        logging.info(f"Image analysis request from {client_ip}: {file.filename}")  # Log the request
        return {"analysis": response}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})


@router.post("/analyze_video/")
async def upload_video(file: UploadFile = File(...), client_ip: str = Header(None)):
    """Upload a video and analyze it for disaster detection."""
    try:
        await rate_limit(client_ip)  # Apply rate limiting

        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        response = analyze_video(file_path)
        logging.info(f"Video analysis request from {client_ip}: {file.filename}")  # Log the request
        return {"analysis": response}
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
