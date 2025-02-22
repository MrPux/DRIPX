from fastapi import APIRouter
from services.firestore_service import store_disaster_data, get_disaster_data

router = APIRouter()

@router.post("/store_data/")
def store_data(category: str, details: str):
    return store_disaster_data(category, details)

@router.get("/get_data/")
def fetch_data():
    return get_disaster_data()