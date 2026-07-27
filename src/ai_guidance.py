import os

from dotenv import load_dotenv
from google import genai

from src.recommendation import get_health_recommendations


# Load environment variables from .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")


# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


def build_health_prompt(health_data):
    """
    Build a grounded prompt using only information
    retrieved from the recommendation datasets.
    """

    return f"""
You are a health-information assistant.

The disease prediction model has identified the following possible condition:

Disease: {health_data["disease"]}

Use ONLY the grounded information provided below to prepare the response.

DESCRIPTION:
{health_data["description"]}

PRECAUTIONS:
{health_data["precautions"]}

TREATMENT / MEDICATION INFORMATION:
{health_data["treatments"]}

DIET:
{health_data["diet"]}

ACTIVITY / WORKOUT:
{health_data["workouts"]}

Instructions:
1. Present the information in clear, simple language.
2. Organize the response into:
   - About the Condition
   - Recommended Precautions
   - Diet Guidance
   - Activity Guidance
   - Treatment / Medication Information
3. Do not diagnose the user.
4. Do not prescribe medications or provide dosages.
5. Do not add medications, treatments, recommendations, or medical facts
   that are not contained in the grounded information.
6. Clearly state that medication and treatment decisions should be made
   with a qualified healthcare professional.
7. End with a short statement that the prediction and recommendations
   are informational and are not a substitute for professional medical
   diagnosis or treatment.
"""


def generate_health_guidance(disease):
    """
    Retrieve grounded health information and enhance its
    presentation using Gemini.
    """

    health_data = get_health_recommendations(disease)

    if health_data is None:
        return None

    prompt = build_health_prompt(health_data)

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text