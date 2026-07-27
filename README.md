# 🩺 AI-Enhanced Disease Prediction and Health Recommendation System

This project is a web-based healthcare application that predicts possible diseases based on user-selected symptoms using a **Machine Learning model**. It also provides personalized health information including precautions, diet, physical activities, and treatment information.

The system integrates **Google Gemini** to transform dataset-grounded recommendations into clear and structured health guidance while ensuring that the generated information remains based on the available recommendation data.

---

## 🚀 Features

- ✅ Predict possible diseases from user-selected symptoms.
- ✅ Supports **230 symptoms** and **100 disease classes**.
- ✅ Displays prediction confidence.
- ✅ Provides disease-specific precautions.
- ✅ Provides diet and activity recommendations.
- ✅ Provides grounded treatment/medication information.
- ✅ Uses **Google Gemini** to generate clear and structured health guidance.
- ✅ Falls back to dataset-based recommendations if the Gemini API is unavailable.
- ✅ Responsive web interface for symptom selection and prediction.

---

## 💡 How It Works

1. **Select Symptoms** — The user searches for and selects the symptoms they are experiencing.
2. **Create Symptom Vector** — The selected symptoms are converted into a 230-feature binary input vector.
3. **Predict Disease** — The trained Machine Learning model predicts the most likely disease.
4. **Calculate Confidence** — The model provides the prediction probability for the predicted disease.
5. **Retrieve Health Information** — Disease-specific descriptions, precautions, medications, diets, and workouts are retrieved from the recommendation datasets.
6. **Generate AI-Enhanced Guidance** — Google Gemini organizes the grounded information into clear health guidance.
7. **Display Results** — The predicted disease, confidence score, and health recommendations are displayed on the web interface.

---

## 🧠 Machine Learning Model

The disease prediction system was developed by comparing multiple Machine Learning algorithms.

| Model | Test Accuracy |
|---|---:|
| Logistic Regression | **89.85%** |
| Bernoulli Naive Bayes | **89.85%** |
| Random Forest | **87.00%** |
| Decision Tree | **85.61%** |

**Logistic Regression** was selected as the final prediction model.

- Training Accuracy: **90.19%**
- Testing Accuracy: **89.85%**
- Top-3 Accuracy: **98.48%**
- Number of Disease Classes: **100**
- Number of Symptom Features: **230**

---

## 📊 Dataset

The main disease prediction dataset contains:

- **96,088 records**
- **230 symptom features**
- **100 unique diseases**
- Binary symptom representation (`0` = absent, `1` = present)

Additional datasets are used to provide grounded health information:

- `description.csv`
- `precautions.csv`
- `medications.csv`
- `diets.csv`
- `workout.csv`

---

## 🤖 AI-Enhanced Health Guidance

After disease prediction, the system retrieves health information directly from the recommendation datasets.

Google Gemini is then provided only with this grounded information and instructed to organize it into:

- About the Condition
- Recommended Precautions
- Diet Guidance
- Activity Guidance
- Treatment / Medication Information

If the Gemini API is unavailable, the application automatically falls back to the original dataset-grounded recommendations instead of failing the entire prediction request.

---

## 🛠️ Tech Stack

- **Python**
- **Flask**
- **Scikit-learn**
- **Pandas**
- **NumPy**
- **Google Gemini API**
- **HTML**
- **CSS**
- **JavaScript**
- **Joblib**

---

## 📁 Project Structure

```text
HealthCare/
│
├── app.py
├── requirements.txt
│
├── data/
│   └── raw/
│       ├── Diseases_and_Symptoms_dataset.csv
│       ├── description.csv
│       ├── precautions.csv
│       ├── medications.csv
│       ├── diets.csv
│       └── workout.csv
│
├── models/
│   ├── disease_prediction_model.pkl
│   ├── label_encoder.pkl
│   └── symptom_features.pkl
│
├── notebooks/
│   ├── 01_Data_Understanding_and_EDA.ipynb
│   ├── 02_Data_Preprocessing_and_Model_Training.ipynb
│   └── 03_Health_Recommendation_System.ipynb
│
├── src/
│   ├── prediction.py
│   ├── recommendation.py
│   └── ai_guidance.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
└── templates/
    └── index.html
