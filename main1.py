import requests
import random

from dotenv import load_dotenv
from weather import weather
# Load environment variables from .env file
load_dotenv()
import os
grok_api_key = os.getenv("GROQ_API_KEY")

# Replace with your Grok API key
GROK_API_URL = "https://api.grok.com/suggestions"  # Replace with the actual Grok API URL
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"  # Example Weather API
WEATHER_API_KEY = "your_openweather_api_key_here"


def get_random_cities():
    """Fetch random cities from the Grok API."""
    try:
        response = requests.get(GROK_API_URL, headers={"Authorization": f"Bearer {grok_api_key}"})
        response.raise_for_status()
        data = response.json()
        # Assume the API returns a list of cities
        cities = data.get("cities", [])
        return random.sample(cities, 3) if len(cities) >= 3 else cities
    except Exception as e:
        print(f"Error fetching cities: {e}")
        return ["New York", "Tokyo", "Paris"]  # Default fallback


def get_weather(city):
    """Fetch weather data for the selected city."""
    try:
        response = requests.get(
            WEATHER_API_URL,
            params={"q": city, "appid": WEATHER_API_KEY, "units": "metric"},
        )
        response.raise_for_status()
        data = response.json()
        weather = data["weather"][0]["description"].capitalize()
        temperature = data["main"]["temp"]
        return f"The weather in {city} is {weather} with a temperature of {temperature}°C."
    except Exception as e:
        return f"Could not fetch weather data for {city}: {e}"


def main():
    print("Hello! Where would you like to travel?")
    cities = get_random_cities()
    print(f"Here are 3 cities you might like: {', '.join(cities)}")

    user_city = input("Please select a city from the list: ").strip()
    if user_city not in cities:
        print("Invalid choice. Please select a city from the list.")
        return

    print("Okay! Fetching weather information for your selected city...")
    # weather_info = 
    weather(user_city)
    # print(weather_info)


if __name__ == "__main__":
    main()
