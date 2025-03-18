import requests
import pandas as pd

def calender(flights_details):
    
    try:
        # Ensure all datetime fields are formatted correctly
        def format_datetime(dt):
            if isinstance(dt, pd.Timestamp):  # If it's a Pandas Timestamp
                return dt.strftime("%Y-%m-%d %H:%M")
            elif isinstance(dt, str):  # If it's a string, try converting it
                try:
                    return pd.to_datetime(dt).strftime("%Y-%m-%d %H:%M")
                except:
                    raise ValueError(f"Invalid datetime format: {dt}")
            else:
                raise ValueError(f"Unexpected datetime type: {type(dt)}")  # Catch dictionaries or lists

        # Step 1: Generate ICS file
        url = "https://calendar-ics-api.azurewebsites.net/generate-ics"
        payload = {
            "outbound_flight_number": str(flights_details["Flight Number"]),
            "outbound_departure_airport": str(flights_details["Departure Airport"]),
            "outbound_arrival_airport": str(flights_details["Arrival Airport"]),
            "outbound_departure_time": format_datetime(flights_details["Departure Time"]),
            "outbound_arrival_time": format_datetime(flights_details["Arrival Time"]),
            "inbound_flight_number": str(flights_details["Flight Number"]),
            "inbound_departure_airport": str(flights_details["Arrival Airport"]),
            "inbound_arrival_airport": str(flights_details["Departure Airport"]),
            "inbound_departure_time": format_datetime(flights_details["Arrival Time"]),
            "inbound_arrival_time": format_datetime(flights_details["Departure Time"])
        }

        print("calender")

        text = ""
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            data = response.json()
            # print(data)
            download_url = "https://calendar-ics-api.azurewebsites.net" + data["download_url"]
            text = f"Download the ICS file from: {download_url}"
            print(text)
            # Step 2: Download the ICS file
            ics_response = requests.get(download_url)
            if ics_response.status_code == 200:
                with open("flight_schedule.ics", "wb") as f:
                    f.write(ics_response.content)
                print("ICS file downloaded successfully as 'flight_schedule.ics'")
            else:
                print("Failed to download ICS file.")

        else:
            print(response.status_code)
            print("Response:", response.text)  # Print error message from API
            print("Failed to generate ICS file.")
    
    except Exception as e:
        print("Exception: ", e)

    return text

