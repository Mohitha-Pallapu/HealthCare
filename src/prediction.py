from pathlib import Path

import joblib
import numpy as np
import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_ROOT / "models"


# Load trained artifacts
prediction_model = joblib.load(
    MODEL_DIR / "disease_prediction_model.pkl"
)

label_encoder = joblib.load(
    MODEL_DIR / "label_encoder.pkl"
)

symptom_features = joblib.load(
    MODEL_DIR / "symptom_features.pkl"
)


def create_symptom_vector(selected_symptoms):
    """
    Convert selected symptom names into the 230-feature
    input format expected by the trained model.
    """

    selected_symptoms = {
        symptom.strip().lower()
        for symptom in selected_symptoms
    }

    input_data = pd.DataFrame(
        [np.zeros(len(symptom_features), dtype=int)],
        columns=symptom_features
    )

    for symptom in selected_symptoms:
        if symptom in input_data.columns:
            input_data.loc[0, symptom] = 1

    return input_data


def predict_disease(selected_symptoms):
    """
    Predict the most likely disease and return the
    model confidence score.
    """

    input_data = create_symptom_vector(selected_symptoms)

    predicted_class = prediction_model.predict(input_data)[0]

    predicted_disease = label_encoder.inverse_transform(
        [predicted_class]
    )[0]

    probabilities = prediction_model.predict_proba(input_data)[0]
    confidence = probabilities[predicted_class]

    return {
        "disease": predicted_disease,
        "confidence": float(confidence)
    }