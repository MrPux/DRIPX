import google.generativeai as genai
from PIL import Image
import io
import cv2
import os
from tempfile import NamedTemporaryFile
from config.settings import GEMINI_API_KEY

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def analyze_image(image_path: str):
    """Analyze an image using Gemini API to detect disasters."""
    try:
        # Open image using PIL
        with open(image_path, "rb") as image_file:
            image = Image.open(io.BytesIO(image_file.read()))  # Convert bytes to PIL Image

        # Use Gemini 1.5 Flash for vision analysis
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Generate AI response
        response = model.generate_content([
            "Identify the disaster in this image and suggest prevention strategies.",
            image
        ])

        return response.text if response else "No response from Gemini."

    except Exception as e:
        return f"Gemini API Error: {str(e)}"

def summarize_video_description(frame_descriptions):
    """Generate a summary of the video based on frame analyses using Gemini AI."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Concatenate frame descriptions into one input text
        full_text = "Summarize the following video analysis based on different frames:\n\n" + "\n".join(frame_descriptions)

        # Request summary from Gemini AI
        response = model.generate_content(full_text)

        return response.text if response else "No summary generated."

    except Exception as e:
        return f"Gemini API Error during summary: {str(e)}"

def analyze_video(video_path: str, frame_interval=90):
    """Extract key frames from a video, analyze them, and generate a summary."""
    
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    insights = []

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Process every nth frame (default = every 90 frames)
            if frame_count % frame_interval == 0:
                with NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
                    frame_path = temp_file.name
                    cv2.imwrite(frame_path, frame)  # Save frame temporarily
                    
                    # Analyze frame using Gemini AI
                    response = analyze_image(frame_path)
                    insights.append(f"Frame {frame_count}: {response}")

                    os.remove(frame_path)  # Clean up the temp file after analysis

            frame_count += 1

        cap.release()

        # Generate a final summarized report based on all analyzed frames
        final_summary = summarize_video_description(insights)

        return {

            "final_summary": final_summary
        }

    except Exception as e:
        return {"status": "Error", "message": f"Video Analysis Error: {str(e)}"}