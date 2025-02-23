import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.markdown(
    """
    <style>
    button
    {
        color:black;
    }
    .stApp {
        background: linear-gradient(#000000, #000000, #062b44) !important;
        color: white;
    }
    h1, h2, h3, h4, h5, h6, p, div, span, label,   {
        color: white;
    }
    .stTextInput>div>div>input, .stFileUploader>div>div>button {
        color: white;
    }
    .stButton>button {
        background-color: white;
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌍 SafeCRASH - AI Disaster Detection")

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

st.header("🖼️ Upload an Image for AI Analysis")
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
    if st.button("Analyze Image"):
        files = {"file": ("image.jpg", uploaded_image.getvalue(), "image/jpeg")}
        response = requests.post(f"{BACKEND_URL}/analyze_image/", files=files)
        
        if response.status_code == 200:
            st.write(response.json()["analysis"])
        else:
            st.error(f"Error analyzing image. Server Response: {response.text}")

st.header("🎥 Upload a Video for AI Analysis")
uploaded_video = st.file_uploader("Choose a video...", type=["mp4", "mov", "avi"])

if uploaded_video:
    st.video(uploaded_video)
    if st.button("Analyze Video"):
        files = {"file": uploaded_video.getvalue()}
        response = requests.post(f"{BACKEND_URL}/analyze_video/", files=files)
        
        if response.status_code == 200:
            analysis = response.json().get("analysis", "No analysis available.")
            
            # Check if analysis is a list or dictionary
            if isinstance(analysis, list):
                analysis_text = "\n\n".join(analysis)  # Convert list to readable text
            elif isinstance(analysis, dict):
                analysis_text = "\n\n".join(f"**{key}:** {value}" for key, value in analysis.items())  # Format dictionary
            else:
                analysis_text = analysis  # If already a string
            
            # Display the formatted text output
            st.markdown(f"### Video Analysis Summary:\n\n{analysis_text}")

        else:
            st.error("Error analyzing video.") 