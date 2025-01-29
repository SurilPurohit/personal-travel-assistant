import random
import requests
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
import os
grok_api_key = os.getenv("GROQ_API_KEY")

def get_random_countries(country_list, n=3):
    """Select n random countries from the given list."""
    return random.sample(country_list, n)

def get_weather_data(country):
    """Fetch weather data using Grok API for the given country."""
    api_url = f"https://api.grok.com/weather?location={country}"  # Replace with the actual Grok API URL
    headers = {
        'Authorization': 'Bearer grok_api_key'  # Replace with your actual API key
    }
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def main():
    countries = ["France", "Japan", "Brazil", "Australia", "Canada", "India", "Italy", "South Korea", "Germany", "Spain"]

    print("Hello! Where would you like to travel? Here are some suggestions:")
    suggestions = get_random_countries(countries)

    for i, country in enumerate(suggestions, 1):
        print(f"{i}. {country}")

    while True:
        try:
            choice = int(input("Select a country by entering the number (1-3): "))
            if choice < 1 or choice > 3:
                raise ValueError("Invalid choice. Please select a number between 1 and 3.")
            selected_country = suggestions[choice - 1]
            break
        except ValueError as e:
            print(e)

    print(f"You selected: {selected_country}. Let me check the weather for you...")

    weather_data = get_weather_data(selected_country)

    if "error" in weather_data:
        print(f"Sorry, I couldn't fetch the weather data. Error: {weather_data['error']}")
    else:
        print(f"Weather in {selected_country}: {weather_data}")

if __name__ == "__main__":
    main()
