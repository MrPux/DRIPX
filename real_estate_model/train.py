import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib
import os

# ----------------------------------------------------------------
# Configuration: file path and column definitions
# ----------------------------------------------------------------
CSV_PATH = "../data/disaster_data.csv"
CHECKPOINT_DIR = "./checkpoint"
CHECKPOINT_NAME = "real_estate_prediction_checkpoint.pkl"
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

INPUT_COLS = [
    "state",
    "declarationType",
    "incidentType"
]

OUTPUT_COLS = [
    "percent_change_in_re"
]

# ----------------------------------------------------------------
# Preprocessing Function
# ----------------------------------------------------------------
def preprocess_data(csv_path=CSV_PATH, input_cols=INPUT_COLS, output_cols=OUTPUT_COLS, fillna_value=0.0):
    df = pd.read_csv(csv_path)
    df = df[input_cols + output_cols]
    df = df.dropna(subset=output_cols)
    df[input_cols] = df[input_cols].fillna(fillna_value)

    categorical_fields = ['state','declarationType', 'incidentType']
    df_encoded = pd.get_dummies(df, columns=categorical_fields, drop_first=True)

    for col in output_cols:
        df_encoded[col] = pd.to_numeric(df_encoded[col], errors='coerce').fillna(fillna_value)

    X = df_encoded.drop(columns=output_cols).values
    Y = df_encoded[output_cols].values
    return X, Y

# ----------------------------------------------------------------
# Main: Preprocess data, split, train, evaluate, and checkpoint MLP regressor
# ----------------------------------------------------------------
if __name__ == "__main__":
    X, Y = preprocess_data()

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    mlp_regressor = MLPRegressor(
        hidden_layer_sizes=(100, 50),
        activation='relu',
        solver='adam',
        max_iter=500,
        early_stopping=True,
        validation_fraction=0.3,
        random_state=42
    )

    mlp_regressor.fit(X_train_scaled, Y_train.ravel())

    Y_pred = mlp_regressor.predict(X_test_scaled)

    mse = mean_squared_error(Y_test, Y_pred)
    r2 = r2_score(Y_test, Y_pred)

    final_training_loss = mlp_regressor.loss_curve_[-1]

    checkpoint_path = os.path.join(CHECKPOINT_DIR, CHECKPOINT_NAME)

    if mlp_regressor.best_loss_ is not None:
        val_loss = mlp_regressor.best_loss_
        joblib.dump(mlp_regressor, checkpoint_path)
        print("Checkpoint saved with Validation Loss:", val_loss)
    elif not os.path.exists(checkpoint_path):
        joblib.dump(mlp_regressor, checkpoint_path)
        print("Checkpoint saved despite no improvement.")
    else:
        print("No improvement in validation loss, no checkpoint saved.")

    print("\nMLP Regressor Performance:")
    print("Mean Squared Error:", mse)
    print("R^2 Score:", r2)
    print("Final Training Loss:", final_training_loss)
    print("Best Validation Loss:", mlp_regressor.best_loss_)
