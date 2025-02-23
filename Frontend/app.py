import streamlit as st

# Set page configuration
st.set_page_config(page_title="Home", layout="wide")

# Custom CSS using st.markdown() with raw HTML
st.markdown("""
    <style>
    /* Background Gradient */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(#062b44,#000000,  #000000) !important;
        color: white !important;
    }

    /* Hide Streamlit Sidebar */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none;
    }

    /* Centering the Main Title */
    .title-container {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: white;
        margin-bottom: 20px;
    }

    /* Glassmorphic Containers */
    .glass-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        color: white;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 10px;
    }

    .glass-container:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: translateY(-5px);
    }

    /* Button Styling */
    .custom-button {
        margin-left:50px;
        background-color: #6A11CB;
        color: white !important;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        padding: 12px 20px;
        cursor: pointer;
        transition: 0.3s ease-in-out;
        border: none;
        display: inline-block;
        text-decoration: none;
        text-align: center;
    }

    .custom-button:hover {
        background-color: #2575fc;
        transform: scale(1.05);
    }
            
   .stButton>button {
        margin-left:390px;
        background-color: white;
        color: black !important;
    }            

    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='title-container'>DRIPX</div>", unsafe_allow_html=True)

st.write("")

st.markdown("<div class='title-container'>Disaster Risk & Insurance Prediction eXpert</div>", unsafe_allow_html=True)

st.write("")

# Glassmorphic Layout with 2 rows of clickable containers
col1, col2 = st.columns(2)
with col1:
    st.markdown("<div class='glass-container'>SafeCrash - AI Disaster Detection</div>", unsafe_allow_html=True)
    if st.button("Explore SafeCrash", key="btn_safecrash"):
        st.switch_page("pages/appDisasterDetection.py")

with col2:
    st.markdown("<div class='glass-container'>Page 2 (Coming Soon)</div>", unsafe_allow_html=True)
    if st.button("View Page 2", key="btn_page2"):
        st.switch_page("pages/page2.py")

st.write("")

col3, col4 = st.columns(2)
with col3:
    st.markdown("<div class='glass-container'>Page 3 (Coming Soon)</div>", unsafe_allow_html=True)
    if st.button("View Page 3", key="btn_page3"):
        st.switch_page("pages/page3.py")
 