from google.cloud import firestore
from config.firebase_config import db

def store_disaster_data(category: str, details: str):
    """ Store disaster-related insights in Firestore """
    doc_ref = db.collection("disaster_recovery").document(category)
    doc_ref.set({"details": details})
    return {"message": "Data stored successfully"}

def get_disaster_data():
    """ Retrieve stored disaster recovery insights """
    docs = db.collection("disaster_recovery").stream()
    return {doc.id: doc.to_dict() for doc in docs}