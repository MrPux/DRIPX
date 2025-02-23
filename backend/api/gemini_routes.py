from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from services.gemini_service import analyze_image, analyze_video
import json

router = APIRouter()

# Define expected disaster fields
DISASTER_FIELDS = [
    "Disaster Type", "Country", "Region",
    "Magnitude", "Magnitude Scale", "CPI",
    "Start Year", "Start Month", "Start Day",
    "End Year", "End Month", "End Day"
]

def extract_disaster_data(response_text):
    """Extract disaster-related fields from AI response JSON."""
    
    expected_fields = [
        "Disaster Type", "Country", "Region",
        "Magnitude", "Magnitude Scale", "CPI",
        "Start Year", "Start Month", "Start Day",
        "End Year", "End Month", "End Day"
    ]
    
    try:
        print("📝 AI Raw Response:\n", response_text)  # Debugging

        # Convert AI response to JSON
        disaster_data = json.loads(response_text)
        
        # Debugging: Print parsed JSON
        print("✅ Parsed Disaster Data:\n", disaster_data)

        # Initialize structured data
        structured_data = {field: disaster_data.get(field, "") for field in expected_fields}

    except json.JSONDecodeError:
        print("⚠️ Error: AI response is not valid JSON:", response_text)
        structured_data = {field: "" for field in expected_fields}  

    return structured_data

@router.post("/analyze_image/")
async def analyze_uploaded_image(file: UploadFile = File(...)):
    try:
        image_path = f"temp_{file.filename}"
        with open(image_path, "wb") as img_file:
            img_file.write(file.file.read())

        # Analyze image with Gemini AI
        response_text = analyze_image(image_path)
        
        print("🔍 Gemini AI Response:", response_text)  # Debugging

        # Extract structured disaster data
        disaster_data = extract_disaster_data(response_text)

        print("✅ Final Structured Data:", disaster_data)  # Debugging

        return JSONResponse(content={"analysis": disaster_data}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.post("/analyze_video/")
async def analyze_uploaded_video(file: UploadFile = File(...)):
    try:
        video_path = f"temp_{file.filename}"
        with open(video_path, "wb") as vid_file:
            vid_file.write(file.file.read())

        # Analyze the video with Gemini AI
        response_text = analyze_video(video_path)

        print("🔍 Gemini AI Response:\n", response_text)  # Debugging: Print the response

        # Extract structured disaster data
        disaster_data = extract_disaster_data(response_text)

        return JSONResponse(content={"analysis": disaster_data}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)