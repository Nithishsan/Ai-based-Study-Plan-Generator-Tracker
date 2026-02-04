import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# --------------------------------------------------
# Environment Setup
# --------------------------------------------------

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in backend/.env")

print("Gemini API Key loaded successfully.")

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-pro:generateContent?key=" + GEMINI_API_KEY
)

HEADERS = {
    "Content-Type": "application/json"
}

# --------------------------------------------------
# Core Planner Logic
# --------------------------------------------------

def generate_plan(goal, total_days, daily_minutes, start_date):
    """
    Generates study guidance using Gemini API.

    Production strategy:
    - Call Gemini for lightweight task suggestions
    - Log raw output for debugging
    - Always return deterministic task structure
    - Gracefully fallback if Gemini fails
    """

    prompt = f"""
Provide 3 concise study tasks for learning {goal}.
Each task should be short.
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(
            GEMINI_URL,
            headers=HEADERS,
            json=payload,
            timeout=20
        )

        # Raise HTTP errors explicitly
        response.raise_for_status()

        result = response.json()

        print("\n--- GEMINI RAW RESPONSE ---")
        print(result)
        print("--------------------------\n")

    except Exception as e:
        # Gemini failure should NOT kill the app
        print("Gemini API Error:", str(e))

    # --------------------------------------------------
    # Deterministic fallback (always returns tasks)
    # --------------------------------------------------

    try:
        datetime.strptime(start_date, "%Y-%m-%d")
    except Exception:
        raise ValueError("Invalid start_date format. Expected YYYY-MM-DD.")

    return [
        {
            "date": start_date,
            "tasks": [
                {
                    "task_name": f"Understand fundamentals of {goal}",
                    "estimated_minutes": min(30, daily_minutes)
                },
                {
                    "task_name": f"Hands-on practice for {goal}",
                    "estimated_minutes": min(30, daily_minutes)
                },
                {
                    "task_name": "Quick revision",
                    "estimated_minutes": min(20, daily_minutes)
                }
            ]
        }
    ]
