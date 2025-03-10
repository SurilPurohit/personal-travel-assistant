from calender_api.calender import calender
from grok_api.beautify_flight import beautify_flight
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

    # Check if response contains expected data
    if "best_flights" not in results or not results["best_flights"]:
        print("Warning: No 'best_flights' data found in API response.")
        return None  # Return None instead of breaking the code

    return results


def process_flight_data(flight_response, i=0):
    if not flight_response or "best_flights" not in flight_response:
        print("Error: No valid flight data to process.")
        return pd.DataFrame()  # Return empty DataFrame instead of raising an error

    try:
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

    except KeyError as e:
        print(f"Error: Missing expected key {e} in flight data.")
        return pd.DataFrame()  # Return empty DataFrame to avoid crashing


def flight(city, i, start_date, end_date):
    print(i)
    try:
        departure_airport = 'YYZ'  # input('Enter the departure airport IATA code: ')
        arrival_airport = city_code(city).upper()  # 'BOM' # input('Enter the arrival airport IATA code: ')
        departure_date = start_date  # '2025-02-10' # input('Enter the departure date in this format YYYY-MM-DD: ')
        return_date = end_date  # '2025-02-14' # input('Enter the return date in this format YYYY-MM-DD: ')
        i = 0
        search = search_flights(departure_airport, arrival_airport, departure_date, return_date)

        if not search:
            print("No flight data returned from API.")
            return False  # Exit early if no flights found

        # Process and display
        flights_details = process_flight_data(search, i)

        if flights_details.empty:
            print("No valid flights found, skipping calendar entry.")
            return False  # Skip further processing

        print(flights_details)

        # Check if "best_flights" key exists before accessing
        if "best_flights" in search:
            flight_type = search["best_flights"][i].get("type", "Unknown")
            price = search["best_flights"][i].get("price", "N/A")
        else:
            print("Warning: 'best_flights' data missing, skipping price details.")
            flight_type, price = "Unknown", "N/A"

        # Adding flight details to calendar
        calender(flights_details.iloc[0])

        # beautifying response with the help of grok API
        # print(beautify_flight(flights_details, flight_type, price))

        return True

    except Exception as e:
        # Handle other potential errors
        print("flight exception:", e)
        print(f"No information available, try again after sometime.")
        return False
