import streamlit as st

st.title("DOOM AI")
st.write("Disaster Optimized Oppurtunity Model")

import streamlit as st
import requests
BACKEND_URL = "http://127.0.0.1:8000"
API_URL = "http://127.0.0.1:8000/predict"

st.title("🌍 Disaster Data Collection")

# Collect inputs
disaster_type = st.text_input("Disaster Type")
country = st.text_input("Country")
region = st.text_input("Region")
declaration_type = st.selectbox("Declaration Type", ["FM", "DR", "EM"])
magnitude_scale = st.text_input("Magnitude Scale")

disaster_data = {
    "Disaster Type": disaster_type,
    "Country": country,
    "Region": region,
    "declaration_type": declaration_type,
    "Magnitude Scale": magnitude_scale
}

if st.button("Get Prediction"):
    response = requests.post(API_URL, json=disaster_data)

    if response.ok:
        prediction = response.json()
        st.write(f"Prediction: {prediction['predection']}")
    else:
        st.error(f"Error: {response.text}")
uploaded_image = st.file_uploader("Upload disaster image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
    
    if st.button("Send Image Data"):
        files = {"file": uploaded_image.getvalue()}
        response = requests.post(f"{BACKEND_URL}/save_disaster_data/", files=files)
        
        if response.ok:
            st.success("Data saved successfully!")
        else:
            st.error(f"Error: {response.text}")

uploaded_video = st.file_uploader("Upload disaster video", type=["mp4", "mov", "avi"])

if uploaded_video:
    st.video(uploaded_video)

    if st.button("Send  .Video Data"):
        files = {"file": uploaded_video.getvalue()}
        response = requests.post(f"{BACKEND_URL}/save_disaster_data/", files=files)
        
        if response.ok:
            st.success("Data saved successfully!")
        else:
            st.error(f"Error: {response.text}")



