import google.generativeai as genai
from config.settings import GEMINI_API_KEY

# Configure Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def ask_gemini(query: str):
    """ Query Google Gemini AI for disaster recovery insights """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"Disaster recovery insights: {query}")
    return response.text