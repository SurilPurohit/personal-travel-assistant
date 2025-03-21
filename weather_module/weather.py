import requests
from datetime import datetime, timedelta

from grok_api.weather_summarize import weather_summarize

# API Endpoints
GEOCODING_API_URL = "https://nominatim.openstreetmap.org/search"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

def get_coordinates(user_city):
    """
    Fetch latitude and longitude for a given user_city using Nominatim API.
    
    Parameters:
    - user_city (str): The name of the city or user_city (e.g., "Mumbai").
    
    Returns:
    - tuple: Latitude and longitude as floats, or None if not found.
    """
    params = {
        "q": user_city,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "PersonalTravelAssistant/1.0 (your_email@example.com)"
    }
    try:
        response = requests.get(GEOCODING_API_URL, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data:
            latitude = float(data[0]["lat"])
            longitude = float(data[0]["lon"])
            return latitude, longitude
        else:
            print("user_city not found.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates: {e}")
        return None

def fetch_weather_forecast(latitude, longitude, start_date, end_date):
    """
    Fetch weather forecast for a range of dates using Open-Meteo API.

    Parameters:
    - latitude (float): Latitude of the user_city.
    - longitude (float): Longitude of the user_city.
    - start_date (str): Start date in YYYY-MM-DD format.
    - end_date (str): End date in YYYY-MM-DD format.

    Returns:
    - dict: Weather forecast data if the request is successful, otherwise None.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,"
                 "windspeed_10m_max,apparent_temperature_max,apparent_temperature_min",
        "timezone": "auto"
    }
    try:
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def display_weather_forecast(data, user_city, start_date, end_date):
    """
    Display the fetched weather forecast data in a readable format.

    Parameters:
    - data (dict): The weather forecast data returned from the API.
    - user_city (str): The name of the user_city.
    - start_date (str): Start date of the forecast range.
    - end_date (str): End date of the forecast range.
    """
    weather_forecast = []

    if data and "daily" in data:
        # print(f"\nWeather forecast for {user_city} from {start_date} to {end_date}:\n")
        weather_forecast.append(f"Weather forecast for {user_city} around {start_date}:")
        daily = data["daily"]
        dates = daily["time"]
        temps_max = daily["temperature_2m_max"]
        temps_min = daily["temperature_2m_min"]
        feels_like_max = daily["apparent_temperature_max"]
        feels_like_min = daily["apparent_temperature_min"]
        precipitation = daily["precipitation_sum"]
        wind_speed = daily["windspeed_10m_max"]

        for i in range(len(dates)):
            # print(f"Date: {dates[i]}")
            weather_forecast.append(f"Date: {dates[i]}")
            # print(f"- Max Temp: {temps_max[i]}°C")
            weather_forecast.append(f"- Max Temp: {temps_max[i]}°C")
            # print(f"- Min Temp: {temps_min[i]}°C")
            weather_forecast.append(f"- Min Temp: {temps_min[i]}°C")
            # print(f"- Feels Like Max: {feels_like_max[i]}°C")
            weather_forecast.append(f"- Feels Like Max: {feels_like_max[i]}°C")
            # print(f"- Feels Like Min: {feels_like_min[i]}°C")
            weather_forecast.append(f"- Feels Like Min: {feels_like_min[i]}°C")
            # print(f"- Precipitation: {precipitation[i]} mm")
            weather_forecast.append(f"- Precipitation: {precipitation[i]} mm")
            # print(f"- Max Wind Speed: {wind_speed[i]} km/h\n")
            weather_forecast.append(f"- Max Wind Speed: {wind_speed[i]} km/h\n")
        
        return weather_summarize(user_city, start_date, weather_forecast)
    else:
        print("No weather forecast data available.")

def weather(user_city, start_date, end_date):
    """
    Main function to get weather forecast for a specified range of dates.
    """
    final_weather_data = ""
    # user_city = input("Enter the user_city name: ")
    coordinates = get_coordinates(user_city)
    if coordinates:
        latitude, longitude = coordinates
        
        if not end_date:
            end_date = start_date + timedelta(days=1)
        
        # Fetch and display the weather forecast
        weather_data = fetch_weather_forecast(latitude, longitude, start_date, end_date)
        final_weather_data = display_weather_forecast(weather_data, user_city, start_date, end_date)
        print(final_weather_data)

    else:
        print("Unable to fetch weather data. Please check the user_city name.")


    return final_weather_data