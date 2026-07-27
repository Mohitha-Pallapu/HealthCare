from flask import Flask, jsonify, request, render_template

from src.prediction import predict_disease, symptom_features
from src.recommendation import get_health_recommendations
from src.ai_guidance import generate_health_guidance


app = Flask(__name__)


def build_fallback_guidance(disease):
    """
    Build grounded health guidance directly from the datasets
    when the Gemini API is unavailable.
    """

    health_data = get_health_recommendations(disease)

    if health_data is None:
        return None

    precautions = "\n".join(
        f"* {item}" for item in health_data["precautions"]
    )

    diet = "\n".join(
        f"* {item}" for item in health_data["diet"]
    )

    workouts = "\n".join(
        f"* {item}" for item in health_data["workouts"]
    )

    treatments = "\n".join(
        f"* {item}" for item in health_data["treatments"]
    )

    return f"""
### About the Condition

{health_data["description"]}

### Recommended Precautions

{precautions}

### Diet Guidance

{diet}

### Activity Guidance

{workouts}

### Treatment / Medication Information

{treatments}

*Treatment and medication decisions should be made with a qualified healthcare professional.*

***

*This prediction and the recommendations are informational and are not a substitute for professional medical diagnosis or treatment.*
""".strip()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/symptoms", methods=["GET"])
def get_symptoms():
    """
    Return all symptom names expected by the ML model.
    """

    return jsonify({
        "symptoms": list(symptom_features)
    })


@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Receive selected symptoms, predict the disease,
    and generate AI-enhanced health guidance.
    """

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is required."
            }), 400

        selected_symptoms = data.get("symptoms", [])

        if not selected_symptoms:
            return jsonify({
                "error": "Please select at least one symptom."
            }), 400

        # -----------------------------------
        # 1. ML Disease Prediction
        # -----------------------------------

        prediction = predict_disease(selected_symptoms)

        disease = prediction["disease"]
        confidence = prediction["confidence"]

        # -----------------------------------
        # 2. AI-Enhanced Health Guidance
        # -----------------------------------

        guidance_source = "ai"

        try:
            guidance = generate_health_guidance(disease)

        except Exception as ai_error:
            print(f"Gemini API unavailable: {ai_error}")

            # Use grounded dataset information instead
            guidance = build_fallback_guidance(disease)
            guidance_source = "fallback"

        # -----------------------------------
        # 3. Recommendation Availability Check
        # -----------------------------------

        if guidance is None:
            return jsonify({
                "error": "Health recommendation data is unavailable."
            }), 404

        # -----------------------------------
        # 4. Successful Response
        # -----------------------------------

        return jsonify({
            "prediction": {
                "disease": disease,
                "confidence": round(confidence * 100, 2)
            },
            "guidance": guidance,
            "guidance_source": guidance_source
        })

    except Exception as error:
        print(f"Prediction error: {error}")

        return jsonify({
            "error": "Unable to process the prediction request."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)