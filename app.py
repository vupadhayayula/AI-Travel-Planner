from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
import time


load_dotenv()
app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("No GEMINI_API_KEY found. Please check the .env file.")

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent"
def get_gemini_travel_plan(travel_data):
    """Generates a travel plan using Google's Gemini API with retries."""
    headers = {
        "Content-Type": "application/json"
    }
    prompt = f"""
    Create a personalized travel itinerary based on the following preferences:
    - Travel Type: {travel_data.get("travelType", "N/A")}
    - Interests: {travel_data.get("interests", "N/A")}
    - Preferred Season: {travel_data.get("season", "N/A")}
    - Duration: {travel_data.get("tripDuration", "N/A")} days
    - Budget: {travel_data.get("budgetRange", "N/A")}

    Provide recommended destinations, activities, and accommodation options.
    """

    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}]
    }

    retries = 3 
    for attempt in range(retries):
        try:
            response = requests.post(
                GEMINI_API_URL,
                headers=headers,
                json=payload,
                params={"key": GEMINI_API_KEY},
                timeout=30 
            )
            response.raise_for_status()
            data = response.json()

            if "candidates" in data and len(data["candidates"]) > 0:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return "Error: Unexpected response format from Gemini API."

        except requests.exceptions.Timeout:
            print(f"⚠️ Timeout: Retrying... ({attempt + 1}/{retries})")
            time.sleep(5) 

        except requests.exceptions.RequestException as e:
            return f"Error communicating with Gemini API: {e}"

    return "Error: Unable to get a response after multiple attempts."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    try:
        travel_data = request.json
        ai_travel_plan = get_gemini_travel_plan(travel_data)
        return jsonify({"plan": ai_travel_plan})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
