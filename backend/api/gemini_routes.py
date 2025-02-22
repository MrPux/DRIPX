from fastapi import APIRouter
from services.gemini_service import ask_gemini

router = APIRouter()

@router.get("/ask/")
def ask_ai(query: str):
    return {"response": ask_gemini(query)}