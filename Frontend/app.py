
import streamlit as st
import requests

# Backend API URL
BACKEND_URL = "http://127.0.0.1:8000"

# Streamlit UI
st.title("🌍 SafeCRASH - Disaster Recovery Dashboard")

# Fetch and Display Disaster Data
st.header("📊 Disaster Insights")

if st.button("Fetch Disaster Data"):
    response = requests.get(f"{BACKEND_URL}/get_data/")
    if response.status_code == 200:
        data = response.json()
        st.json(data)  # Display retrieved disaster data
    else:
        st.error("Failed to fetch disaster data!")

# AI-Powered Disaster Insights
st.header("🤖 AI-Powered Disaster Analysis")
query = st.text_input("Enter a disaster-related question:")
if st.button("Get AI Insights"):
    response = requests.get(f"{BACKEND_URL}/ask/", params={"query": query})
    if response.status_code == 200:
        st.write(response.json()["response"])
    else:
        st.error("Failed to fetch AI insights!")