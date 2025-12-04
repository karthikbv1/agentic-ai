import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from google.colab import userdata


# Get API keys from environment variables

gemini_api_key = userdata.get("GOOGLE_API_KEY")
if not gemini_api_key:
    print("Warning: GEMINI_API_KEY not found. Gemini model will not run.")

import os, requests

GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

def get_weather(city: str, country: str | None = None) -> dict:
    # 1) geocode
    params = {"name": city, "count": 1}
    r = requests.get(GEOCODING_API_URL, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    if not data.get("results"):
        return {"error": f"could not find location for {city}"}
    lat = data["results"][0]["latitude"]
    lon = data["results"][0]["longitude"]
    

    # 2) weather
    w = requests.get(
        FORECAST_URL,
        params={"latitude": lat, "longitude": lon, "current_weather": True},
        timeout=15,
    )
    w.raise_for_status()
    return {
        "city": city,
        "coords": {"lat": lat, "lon": lon},
        "current_weather": w.json().get("current_weather"),
    }


get_weather("tokyo")

