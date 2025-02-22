import os
import firebase_admin
from firebase_admin import credentials, firestore

# Get the absolute path of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_PATH = os.path.join(BASE_DIR, "../serviceAccountKey.json")

# Load Firebase credentials
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()