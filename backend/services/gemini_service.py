import google.generativeai as genai
from PIL import Image
import io
import cv2
import os
from config.settings import GEMINI_API_KEY
import json

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)



def analyze_image(image_path: str):
    """Analyze an image using Gemini API and return structured JSON."""
    try:
        # Open image using PIL
        with open(image_path, "rb") as image_file:
            image = Image.open(io.BytesIO(image_file.read()))  

        # Use Gemini AI model
        model = genai.GenerativeModel("gemini-1.5-flash")

        # AI Prompt: Ensure structured JSON
        prompt = """
        Analyze this image and return disaster details in JSON format:
        {
            "Disaster Type": "Type of disaster (Flood, Earthquake, etc.)",
            "Country": "Country where disaster occurred",
            "Region": "Continent or broad region",
            "Magnitude": "Severity (if applicable)",
            "Magnitude Scale": "Measurement scale (if applicable)",
            "CPI": "Consumer Price Index impact (if available)",
            "Start Year": "Year disaster started",
            "Start Month": "Month disaster started",
            "Start Day": "Day disaster started",
            "End Year": "Year disaster ended",
            "End Month": "Month disaster ended",
            "End Day": "Day disaster ended"
        }
        If any field is unknown, return an empty string "".
        Response must be valid JSON format.
        """

        # Get AI response
        response = model.generate_content([prompt, image])

        # Ensure AI response is a string
        ai_response = response.text if response else "{}"

        print("🔍 Gemini AI Raw Response:\n", ai_response)  # Debugging

        return ai_response

    except Exception as e:
        return json.dumps({"error": f"Gemini API Error: {str(e)}"})  

def analyze_video(video_path: str, frame_interval=90):
    """Extract key frames from a video and analyze them using Gemini AI."""
    
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    insights = []

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                frame = cv2.resize(frame, (640, 480))
                frame_path = f"frame_{frame_count}.jpg"
                cv2.imwrite(frame_path, frame)

                response = analyze_image(frame_path)
                insights.append(response)

                os.remove(frame_path)

            frame_count += 1

        cap.release()
        
        return json.dumps({
            "status": "Success",
            "frames_analyzed": len(insights),
            "results": insights
        })

    except Exception as e:
        return json.dumps({"status": "Error", "message": f"Video Analysis Error: {str(e)}"})