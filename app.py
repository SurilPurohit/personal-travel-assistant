
from calender_api.calender import calender
from flight_recommendations.flight import flight
import streamlit as st
import pandas as pd
import random
import re
from datetime import date, timedelta

from weather_module.weather import weather

# Function to extract city from user input
def extract_city_from_text(text, cities):
    if not text:
        return None
        
    for city in cities:
        if re.search(rf"\b{city}\b", text, re.IGNORECASE):
            return city
            
    # If no predefined city is found, try to extract any potential city name
    # This will allow users to enter cities not in our predefined list
    words = re.findall(r'\b[A-Z][a-z]+\b', text)  # Find words that start with uppercase
    potential_cities = [word for word in words if len(word) > 3]  # Filter out short words
    
    if potential_cities:
        return potential_cities[0]  # Return the first potential city
    
    return None

# Generate fake weather data
# def get_weather(city, start_date, end_date):
#     return f"Weather in {city} from {start_date} to {end_date}: ☀ Sunny, 25°C"

# Generate fake flights
# def search_flights(departure_airport, arrival_airport, departure_date, return_date, flight_class):
#     airlines = ["Air Canada", "Delta", "United Airlines", "Emirates", "Qatar Airways"]
    
#     return [
#         {
#             "Flight Number": f"AC{random.randint(100,999)}",
#             "Airline": random.choice(airlines),
#             "Class": flight_class,
#             "Price": f"${random.randint(200, 1000)}",
#             "Departure": f"{departure_date} 10:00",
#             "Arrival": f"{departure_date} 12:00",
#             "Return Flight": f"AC{random.randint(100,999)}" if return_date else "N/A",
#             "Return Departure": f"{return_date} 15:00" if return_date else "N/A",
#             "Return Arrival": f"{return_date} 17:00" if return_date else "N/A",
#         }
#         for _ in range(3)  # Generate 3 fake flight options
#     ]

# Generate itinerary with city history (static for now)
def generate_itinerary(flight, city):
    city_history = {
        "New York": [
            "Founded in 1624 by Dutch settlers.",
            "Home to the Statue of Liberty, Times Square, and Wall Street.",
            "One of the most culturally diverse cities in the world.",
        ],
        "Paris": [
            "Known as the 'City of Light'.",
            "Home to the Eiffel Tower and Louvre Museum.",
            "A global hub for fashion, gastronomy, and art.",
        ],
        "Tokyo": [
            "Capital of Japan since 1868.",
            "Blend of traditional temples and cutting-edge technology.",
            "Famous for its cherry blossoms and bustling Shibuya Crossing.",
        ],
        "Los Angeles": [
            "Entertainment capital of the world.",
            "Home to Hollywood and the Walk of Fame.",
            "Known for its year-round warm weather and beaches.",
        ],
        "London": [
            "Capital of England and the United Kingdom.",
            "Home to Buckingham Palace and the Tower of London.",
            "Known for its rich history and diverse culture.",
        ],
        "Dubai": [
            "City of superlatives with the world's tallest building, Burj Khalifa.",
            "Transformed from a fishing village to a global city in just decades.",
            "Known for luxury shopping, ultramodern architecture, and lively nightlife.",
        ],
        "Sydney": [
            "Australia's oldest and largest city.",
            "Famous for its Opera House and Harbour Bridge.",
            "Known for its beautiful beaches and outdoor lifestyle.",
        ],
        "Rome": [
            "Italy's capital with a history spanning 28 centuries.",
            "Home to the Colosseum, the Pantheon, and Vatican City.",
            "Known as the 'Eternal City' and birthplace of Western civilization.",
        ],
        "Bangkok": [
            "Capital and most populous city of Thailand.",
            "Known for ornate shrines, vibrant street life, and floating markets.",
            "A major center for shopping and dining in Southeast Asia.",
        ],
        "Toronto": [
            "Canada's largest city and a global center for business and culture.",
            "Home to the iconic CN Tower and diverse neighborhoods.",
            "Known for its multiculturalism with over 200 ethnic groups.",
        ]
    }

    # Get history points for the selected city, or provide a generic message if city not found
    history_points = city_history.get(city, [
        f"Discover the unique history of {city}.",
        f"Explore the local culture and attractions in {city}.",
        f"Experience the authentic cuisine and hospitality of {city}."
    ])

    return f"""
    ## 📝 Your Itinerary  
    - **Airline:** {flight['Airline']}  
    - **Flight Number:** {flight['Flight Number']}  
    - **Class:** {flight['Class']}  
    - **Departure:** {flight['Departure']}  
    - **Arrival:** {flight['Arrival']}  
    - **Return Flight:** {flight['Return Flight']}  
    - **Return Departure:** {flight['Return Departure']}  
    - **Return Arrival:** {flight['Return Arrival']}  
    - **Total Price:** {flight['Price']}  
    ---
    ## 🏙 About {city}  
    - {history_points[0]}  
    - {history_points[1]}  
    - {history_points[2]}  
    🎉 Enjoy your trip!
    """

# Function to generate fake calendar invite link
# def generate_calendar_link():
#     return "[📅 Download Calendar Invite](#)"

# Set up Streamlit page
st.set_page_config(page_title="Vacation Voyager", layout="wide")
st.title("✈ Vacation Voyager Dashboard")
st.markdown("Plan your perfect trip in just a few clicks! 🚀")

# Define session state
if "flights" not in st.session_state:
    st.session_state.flights = []
if "selected_flight" not in st.session_state:
    st.session_state.selected_flight = None
if "disable_selection" not in st.session_state:
    st.session_state.disable_selection = False  # Flag to disable selection after choosing a flight
if "destination_city" not in st.session_state:
    st.session_state.destination_city = None  # Store the selected destination city

# Sidebar for user input
st.sidebar.header("🌍 Trip Details")

cities = ["New York", "Los Angeles", "Toronto", "London", "Paris", "Tokyo", "Dubai", "Sydney", "Rome", "Bangkok"]

# Ask user how they want to input their destination
destination_input_method = st.sidebar.radio("How would you like to select your destination?", ["Enter text", "Use dropdown"])

if destination_input_method == "Enter text":
    user_text = st.sidebar.text_area("Enter your trip details (e.g., 'I want to travel to Tokyo next week'):")
    detected_city = extract_city_from_text(user_text, cities)
    
    # Always disable the dropdown when "Enter text" is selected, regardless of whether a city is detected
    dropdown_disabled = True
    
    if detected_city:
        st.sidebar.success(f"Detected destination: {detected_city}")
        city = detected_city
        # For UI consistency, still show the dropdown but keep it disabled
        st.sidebar.selectbox("Available destinations (disabled):", cities, 
                           index=cities.index(detected_city) if detected_city in cities else 0, 
                           disabled=dropdown_disabled)
    else:
        # If no city detected in text, show a notice but keep dropdown disabled
        if user_text:
            st.sidebar.warning("No specific destination detected. Please try entering a city name more clearly.")
            city = None  # No city detected yet
        else:
            city = None  # No text entered yet
            
        # Show disabled dropdown
        st.sidebar.selectbox("Available destinations (disabled):", cities, index=0, disabled=dropdown_disabled)
else:
    # If dropdown selected, just show the dropdown with no text input
    dropdown_disabled = False
    city = st.sidebar.selectbox("Select your destination:", cities, index=0, disabled=dropdown_disabled)

# Store the selected city
st.session_state.destination_city = city

passengers = st.sidebar.slider("Number of Passengers", 1, 10, 1)

trip_type = st.sidebar.radio("Trip Type", ["Single Trip", "Round Trip"])

flight_class = st.sidebar.radio("Flight Class", ["Economy", "Premium Economy", "Business", "First Class"])

start_date = st.sidebar.date_input("Departure Date", date.today())
min_end_date = start_date + timedelta(days=1)
end_date = st.sidebar.date_input("Return Date", min_end_date, min_value=min_end_date, disabled=(trip_type == "Single Trip"))

if trip_type == "Single Trip":
    end_date = None  # Disable return date for Single Trip

# Search Flights Button
if st.sidebar.button("🔍 Search Flights"):
    # Validate that we have a destination city before proceeding
    if city is None:
        st.sidebar.error("Please enter a valid destination or switch to dropdown selection.")
    else:
        # Store the destination city at the time of search
        st.session_state.destination_city = city
        
        # If it's a custom city (not in our predefined list)
        if city not in cities:
            st.sidebar.info(f"Searching for flights to {city}. This destination may have limited information available.")
        
        st.session_state.flights = flight("YYZ", city, start_date, end_date, flight_class)
        st.session_state.selected_flight = None  # Reset selection on new search
        st.session_state.disable_selection = False  # Re-enable selection when searching again

# Display Weather
if st.session_state.flights:
    st.subheader(f"⛅ Weather Forecast for {city}")
    st.info(weather(city, start_date, end_date))

    # Show Flights
    st.subheader("✈ Available Flights")
    # df_flights = pd.DataFrame(st.session_state.flights)
    # st.dataframe(df_flights)

    # Flight Selection with Persistence
    st.subheader("📌 Select a Flight")
    # flight_options = [f"{flight['Airline']} | {flight['Flight Number']} | {flight['Price']}" for flight in st.session_state.flights]
    
    # selected_flight_index = st.radio(
    #     "Choose your flight:", 
    #     list(range(len(flight_options))), 
    #     format_func=lambda x: flight_options[x], 
    #     index=None if not st.session_state.selected_flight else flight_options.index(f"{st.session_state.selected_flight['Airline']} | {st.session_state.selected_flight['Flight Number']} | {st.session_state.selected_flight['Price']}"),
    #     disabled=st.session_state.disable_selection  # Disable selection after choosing a flight
    # )

    # if selected_flight_index is not None and not st.session_state.disable_selection:
    #     st.session_state.selected_flight = st.session_state.flights[selected_flight_index]
    #     st.session_state.disable_selection = True  # Lock selection after choosing a flight

# Show Itinerary & Calendar Download
if st.session_state.selected_flight:
    st.subheader("📝 Your Itinerary")
    st.success("Flight Selected! Generating Itinerary...")
    
    # Use the destination city that was saved when searching for flights
    # This ensures we use the city that was active during flight search
    destination = st.session_state.destination_city
    
    # Display which city's information is being shown
    st.info(f"Showing information for: {destination}")
    
    # Generate and display the itinerary
    st.markdown(generate_itinerary(st.session_state.selected_flight, destination), unsafe_allow_html=True)
    
    # Calendar Download Option
    st.subheader("📅 Calendar Invite")
    # st.markdown(calender(), unsafe_allow_html=True)
else:
    if st.session_state.flights:
        st.warning("🔄 Not satisfied? Modify your search and try again!")

