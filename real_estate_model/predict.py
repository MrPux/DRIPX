from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Configuration: Define checkpoint path and other constants
CHECKPOINT_DIR = "./checkpoint"
CHECKPOINT_NAME = "real_estate_prediction_checkpoint.pkl"
CHECKPOINT_PATH = os.path.join(CHECKPOINT_DIR, CHECKPOINT_NAME)

# Define the columns used in prediction
INPUT_COLS = [
    "state",
    "declarationType",
    "incidentType"
]

def load_model(checkpoint_path=CHECKPOINT_PATH):
    """
    Load the pre-trained MLP regressor model from the checkpoint.
    """
    if os.path.exists(checkpoint_path):
        model = joblib.load(checkpoint_path)
        print(f"Model loaded from checkpoint: {checkpoint_path}")
        return model
    else:
        print("Checkpoint not found!")
        return None

def preprocess_input_json(input_json, input_cols=INPUT_COLS):
    """
    Preprocess the JSON input data to match the input columns.
    This function assumes the input_json is already in a dictionary format.
    """
    # Extract the input features from JSON
    input_data = []
    for col in input_cols:
        input_data.append(input_json.get(col, 0))  # Default to 0 if key doesn't exist

    # Convert the input data to a DataFrame to handle categorical encoding
    df_input = pd.DataFrame([input_data], columns=input_cols)

    # Apply one-hot encoding to categorical features
    df_encoded = pd.get_dummies(df_input, drop_first=True)

    return df_encoded.values  # Return the numpy array for prediction

def predict_with_model(input_json, model=None):
    """
    Use the loaded model to predict on the input JSON data.
    """
    if model is None:
        print("Model is not loaded!")
        return None

    # Preprocess the JSON data into the format the model expects
    X_input = preprocess_input_json(input_json)

    # Standardize the input features (make sure to use the same scaler from training)
    scaler = StandardScaler()
    X_input_scaled = scaler.fit_transform(X_input)  # Ensure the scaling matches the training process

    # Make predictions using the trained model
    prediction = model.predict(X_input_scaled)
    return prediction[0]  # Return the first prediction as a single value

model = load_model()

class PredictionRequest(BaseModel):
    state: str
    declarationType: str
    incidentType: str

# Define a POST endpoint to receive the prediction request
@app.post("/predict")
async def predict(data: PredictionRequest):
    """
    Receive input JSON, process it, and return prediction result.
    """
    if model is None:
        return {"error": "Model is not loaded!"}

    # Convert the Pydantic model to a dictionary
    input_json = data.dict()

    # Make the prediction using the model
    prediction = predict_with_model(input_json, model)

    if prediction is not None:
        return {"prediction": prediction}
    else:
        return {"error": "Prediction failed."}

# if __name__ == "__main__":
#     # Example input JSON
#     input_json = {
#         "state": "California",
#         "declarationType": "FEMA",
#         "incidentType": "Fire"
#     }
#
#     # Load the trained model from checkpoint
#     model = load_model()
#
#     if model:
#         # Make prediction
#         prediction = predict_with_model(input_json, model)
#         print(f"Prediction for input {input_json}: {prediction}")
