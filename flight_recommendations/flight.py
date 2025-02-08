from grok_api.city_code import city_code
from serpapi import GoogleSearch
import pandas as pd
# Ensure Pandas shows all columns
pd.set_option("display.max_columns", None)

# import ace_tools as tools
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
import os
flight_api_key = os.getenv("FLIGHT_API_KEY")


def search_flights(departure_airport, arrival_airport, departure_date, return_date):
    params = {
        "engine": "google_flights",
        "departure_id": departure_airport,
        "arrival_id": arrival_airport,
        "outbound_date": departure_date,
        "return_date": return_date,
        "currency": "CAD",
        "hl": "en",
        "api_key": flight_api_key
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    
    return results

def process_flight_data(flight_response, i=0):
    flights_data = []

    flights_data = pd.DataFrame([
        {
            "Flight Number": flight["flight_number"],
            "Airline": flight["airline"],
            "Departure Airport": flight["departure_airport"]["name"],
            "Departure Time": flight["departure_airport"]["time"],
            "Arrival Airport": flight["arrival_airport"]["name"],
            "Arrival Time": flight["arrival_airport"]["time"],
            "Duration (min)": flight["duration"],
            "Airplane": flight.get("airplane", "N/A"),
            "Travel Class": flight["travel_class"],
            "Legroom": flight["legroom"],
            "Extensions": ", ".join(flight["extensions"]),
            "Often Delayed": flight.get("often_delayed_by_over_30_min", False),
            "Overnight Flight": flight.get("overnight", False)
        }
        for flight in flight_response['best_flights'][i]["flights"]
    ])

    return flights_data


def flight(city, i=0):
    departure_airport = 'YYZ' # input('Enter the departure airport IATA code: ')
    arrival_airport = city_code(city).upper() # 'BOM' # input('Enter the arrival airport IATA code: ')
    departure_date = '2025-02-10' # input('Enter the departure date in this format YYYY-MM-DD: ')
    return_date = '2025-02-14' # input('Enter the return date in this format YYYY-MM-DD: ')
    i = 0
    search = search_flights(departure_airport, arrival_airport, departure_date, return_date)

    # Process and display
    flights_price_df = process_flight_data(search, i)
    print(flights_price_df)
    print(search["best_flights"][i]["type"])
    print(search["best_flights"][i]["price"])