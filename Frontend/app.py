import streamlit as st
import requests
import json

BACKEND_URL = "http://127.0.0.1:8000"

st.title("🌍 SafeCRASH - AI Disaster Detection")

# ------------------ IMAGE UPLOAD ------------------
st.header("🖼️ Upload an Image for AI Analysis")
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
    if st.button("Analyze Image"):
        files = {"file": ("image.jpg", uploaded_image.getvalue(), "image/jpeg")}
        response = requests.post(f"{BACKEND_URL}/analyze_image/", files=files)
        
        if response.status_code == 200:
            analysis = response.json().get("analysis", {})

            st.subheader("📝 Disaster Analysis Data (Image)")
            st.json(analysis)  

            json_filename = "image_analysis.json"
            st.download_button(label="📥 Download JSON", data=json.dumps(analysis, indent=4),
                               file_name=json_filename, mime="application/json")
        else:
            st.error(f"Error analyzing image. Server Response: {response.text}")

# ------------------ VIDEO UPLOAD ------------------
st.header("🎥 Upload a Video for AI Analysis")
uploaded_video = st.file_uploader("Choose a video...", type=["mp4", "mov", "avi"])

if uploaded_video:
    st.video(uploaded_video)
    if st.button("Analyze Video"):
        files = {"file": uploaded_video.getvalue()}
        response = requests.post(f"{BACKEND_URL}/analyze_video/", files=files)
        
        if response.status_code == 200:
            analysis = response.json().get("analysis", {})

            st.subheader("📝 Disaster Analysis Data (Video)")
            st.json(analysis)  

            json_filename = "video_analysis.json"
            st.download_button(label="📥 Download JSON", data=json.dumps(analysis, indent=4),
                               file_name=json_filename, mime="application/json")
        else:
            st.error("Error analyzing video.")