from flask import Flask, jsonify, request,render_template

from src.prediction import predict_disease
from src.ai_guidance import generate_health_guidance


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/symptoms", methods=["GET"])
def get_symptoms():
    """
    Return all symptom names expected by the ML model.
    """

    from src.prediction import symptom_features

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

        # ML disease prediction
        prediction = predict_disease(selected_symptoms)

        disease = prediction["disease"]
        confidence = prediction["confidence"]

        # AI-enhanced grounded health guidance
        guidance = generate_health_guidance(disease)

        if guidance is None:
            return jsonify({
                "error": "Health recommendation data is unavailable."
            }), 404

        return jsonify({
            "prediction": {
                "disease": disease,
                "confidence": round(confidence * 100, 2)
            },
            "guidance": guidance
        })

    except Exception as error:
        print(f"Prediction error: {error}")

        return jsonify({
            "error": "Unable to process the prediction request."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)