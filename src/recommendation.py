from pathlib import Path
import ast
import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"


# Load recommendation datasets
description_df = pd.read_csv(DATA_DIR / "description.csv")
precautions_df = pd.read_csv(DATA_DIR / "precautions.csv")
medications_df = pd.read_csv(DATA_DIR / "medications.csv")
diets_df = pd.read_csv(DATA_DIR / "diets.csv")
workout_df = pd.read_csv(DATA_DIR / "workout.csv")


def normalize_disease_name(name):
    """
    Normalize disease names so they can be matched
    consistently across datasets.
    """
    return str(name).strip().lower()


# Normalize disease columns
for df in [
    description_df,
    precautions_df,
    medications_df,
    diets_df,
    workout_df
]:
    df["disease_key"] = df["Disease"].apply(normalize_disease_name)


# Resolve known naming mismatch
precautions_df["disease_key"] = precautions_df["disease_key"].replace({
    "copd": "chronic obstructive pulmonary disease (copd)"
})


def parse_list(value):
    """
    Convert list-like CSV strings into Python lists.
    """
    if isinstance(value, list):
        return value

    if pd.isna(value):
        return []

    try:
        parsed = ast.literal_eval(value)

        if isinstance(parsed, list):
            return parsed

        return [str(parsed)]

    except (ValueError, SyntaxError):
        return [str(value)]


# Parse list-based recommendation columns
medications_df["Medication"] = medications_df["Medication"].apply(parse_list)
diets_df["Diet"] = diets_df["Diet"].apply(parse_list)
workout_df["Workouts"] = workout_df["Workouts"].apply(parse_list)


def get_health_recommendations(disease):
    """
    Retrieve grounded health information for a predicted disease.
    """

    disease_key = normalize_disease_name(disease)

    description_row = description_df[
        description_df["disease_key"] == disease_key
    ]

    precautions_row = precautions_df[
        precautions_df["disease_key"] == disease_key
    ]

    medications_row = medications_df[
        medications_df["disease_key"] == disease_key
    ]

    diets_row = diets_df[
        diets_df["disease_key"] == disease_key
    ]

    workout_row = workout_df[
        workout_df["disease_key"] == disease_key
    ]

    # Ensure grounded information exists in every dataset
    if (
        description_row.empty
        or precautions_row.empty
        or medications_row.empty
        or diets_row.empty
        or workout_row.empty
    ):
        return None

    description = description_row.iloc[0]["Description"]

    precautions = precautions_row.iloc[0][
        ["Precaution_1", "Precaution_2", "Precaution_3", "Precaution_4"]
    ].dropna().tolist()

    treatments = medications_row.iloc[0]["Medication"]
    diet = diets_row.iloc[0]["Diet"]
    workouts = workout_row.iloc[0]["Workouts"]

    return {
        "disease": disease,
        "description": description,
        "precautions": precautions,
        "treatments": treatments,
        "diet": diet,
        "workouts": workouts
    }