# 🩺 AI-Enhanced Disease Prediction and Health Recommendation System

A web-based healthcare application that predicts possible diseases based on user-selected symptoms using **Machine Learning** and provides personalized health information including precautions, diet, physical activities, and treatment information.

The system integrates **Google Gemini** to transform dataset-grounded health information into clear, structured, and user-friendly guidance.

---

## 🌐 Live Demo

🚀 **Try the deployed application:**  
https://healthcare-tbhp.onrender.com

📂 **GitHub Repository:**  
https://github.com/Mohitha-Pallapu/HealthCare

> **Note:** The application is hosted on Render's free tier. The first request may take some time if the service has been inactive.

---

## 🚀 Features

- ✅ Predicts possible diseases from user-selected symptoms
- ✅ Supports **230 symptom features** and **100 disease classes**
- ✅ Displays prediction confidence
- ✅ Provides disease-specific descriptions and precautions
- ✅ Provides diet recommendations
- ✅ Provides physical activity/workout guidance
- ✅ Provides treatment and medication information
- ✅ Uses **Google Gemini** for structured AI-enhanced health guidance
- ✅ Grounds AI-generated guidance using information retrieved from project datasets
- ✅ Provides dataset-based fallback guidance if the Gemini API is unavailable
- ✅ Responsive and searchable symptom-selection interface

---

## 💡 How It Works

1. **Select Symptoms** — The user searches for and selects the symptoms they are experiencing.

2. **Create Symptom Vector** — The selected symptoms are converted into a **230-feature binary vector** matching the features used during model training.

3. **Predict Disease** — The trained Logistic Regression model predicts the most likely disease.

4. **Calculate Confidence** — The model's predicted probability is used to display a confidence score.

5. **Retrieve Health Information** — Information related to the predicted disease is retrieved from the description, precaution, medication, diet, and workout datasets.

6. **Generate AI-Enhanced Guidance** — The grounded information is passed to Google Gemini, which organizes it into clear and readable health guidance.

7. **Display Results** — The predicted disease, confidence score, and health recommendations are displayed on the web interface.

---

## 🧠 Machine Learning Model

Multiple Machine Learning algorithms were trained and evaluated for disease prediction.

| Model | Test Accuracy |
|---|---:|
| Logistic Regression | **89.85%** |
| Bernoulli Naive Bayes | **89.85%** |
| Random Forest | **87.00%** |
| Decision Tree | **85.61%** |

**Logistic Regression** was selected as the final disease prediction model.

### 📈 Model Performance

- **Training Accuracy:** 90.19%
- **Testing Accuracy:** 89.85%
- **Top-3 Accuracy:** 98.48%
- **Disease Classes:** 100
- **Symptom Features:** 230

---

## 📊 Dataset

The primary disease prediction dataset contains:

- **96,088 records**
- **230 symptom features**
- **100 unique disease classes**
- Binary symptom representation:
  - `1` → Symptom present
  - `0` → Symptom absent

Additional datasets are used to retrieve disease-specific health information:

- `description.csv`
- `precautions.csv`
- `medications.csv`
- `diets.csv`
- `workout.csv`

These datasets provide the grounded information used by the health recommendation system.

---

## 🤖 AI-Enhanced Health Guidance

The Machine Learning model is responsible for **disease prediction**, while Google Gemini is used to enhance the presentation of the health recommendations.

After a disease is predicted, the application retrieves relevant information from the recommendation datasets.

This grounded information is provided to Gemini and organized into:

- **About the Condition**
- **Recommended Precautions**
- **Diet Guidance**
- **Activity Guidance**
- **Treatment / Medication Information**

Gemini is instructed to work only with the supplied grounded information and not independently determine the predicted disease.

If the Gemini API is temporarily unavailable, the application falls back to the original **dataset-grounded recommendations**, allowing the core prediction system to continue functioning.

---

## 🛠️ Tech Stack

### Machine Learning & Data Processing

- Python
- Scikit-learn
- Pandas
- NumPy
- Joblib

### Generative AI

- Google Gemini API
- Google GenAI Python SDK

### Backend

- Flask
- Gunicorn

### Frontend

- HTML
- CSS
- JavaScript

### Deployment

- Render
- GitHub

---

## 🔄 System Architecture

```text
User Selects Symptoms
        ↓
Flask Web Application
        ↓
230-Feature Binary Symptom Vector
        ↓
Logistic Regression Model
        ↓
Disease Prediction + Confidence
        ↓
Health Recommendation Retrieval
        ↓
┌─────────────────────────────────────────────┐
│ Description                                 │
│ Precautions                                 │
│ Diet                                        │
│ Medication / Treatment Information          │
│ Workout / Activity Guidance                 │
└─────────────────────────────────────────────┘
        ↓
Google Gemini
        ↓
AI-Enhanced Grounded Health Guidance
        ↓
Web Interface


If Gemini is unavailable:

Grounded Recommendation Data
        ↓
Dataset-Based Fallback
        ↓
Web Interface
```

---

## 📁 Project Structure

```text
HealthCare/
│
├── app.py
├── requirements.txt
├── .gitignore
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
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Mohitha-Pallapu/HealthCare.git
cd HealthCare
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Gemini API Key

Create a `.env` file in the root directory of the project:

```env
GEMINI_API_KEY=your_gemini_api_key
```

> ⚠️ Never commit the `.env` file or expose your Gemini API key publicly.

### 6. Run the Application

```bash
python app.py
```

### 7. Open the Application

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

---

## 🔌 API Endpoints

### Get Available Symptoms

```http
GET /api/symptoms
```

Returns the symptom features supported by the trained Machine Learning model.

### Predict Disease

```http
POST /api/predict
```

Example request:

```json
{
  "symptoms": [
    "anxiety and nervousness",
    "shortness of breath",
    "chest tightness",
    "palpitations"
  ]
}
```

The endpoint returns:

- Predicted disease
- Model confidence
- Health guidance
- Guidance source (`ai` or `fallback`)

---

## 📸 Application Screenshots

### Symptom Selection Interface

<img width="1429" height="737" alt="image" src="https://github.com/user-attachments/assets/652dd3f0-3040-4a66-a332-dee81d34a343" />
<img width="1423" height="510" alt="image" src="https://github.com/user-attachments/assets/be6db96e-d8c3-4350-9852-83644a1a1e23" />



### Prediction Result

<img width="1324" height="571" alt="image" src="https://github.com/user-attachments/assets/d842a6ea-b0ff-4e1c-b01b-65a78c1a985c" />
<img width="1036" height="788" alt="image" src="https://github.com/user-attachments/assets/dc85db1b-f63d-4c30-9abf-b45465200b2e" />
<img width="747" height="370" alt="image" src="https://github.com/user-attachments/assets/1fdef9db-aa9a-4cb7-a33f-71848a78aa02" />
<img width="1083" height="757" alt="image" src="https://github.com/user-attachments/assets/fbfda45d-6e16-4c5d-87e5-464e71eb6e70" />

---

## ⚠️ Medical Disclaimer

This application was developed for **educational and informational purposes only**.

The disease predictions and health recommendations provided by this system are **not a substitute for professional medical diagnosis, advice, or treatment**.

The predicted condition should be treated only as a Machine Learning prediction based on the symptoms provided by the user.

Medication and treatment decisions should always be made in consultation with a qualified healthcare professional.

---

## 🔮 Future Improvements

- Display **Top-3 disease predictions** on the web interface
- Add model explainability and symptom contribution analysis
- Add user authentication and prediction history
- Expand and professionally validate the health recommendation datasets
- Evaluate additional Machine Learning and ensemble approaches
- Improve monitoring and error handling for external AI services
- Add additional validation for unusual or insufficient symptom combinations
