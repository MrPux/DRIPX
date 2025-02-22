import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.title("🌍 SafeCRASH - AI Disaster Detection")

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
            st.write(response.json()["analysis"])
        else:
            st.error("Error analyzing video.")