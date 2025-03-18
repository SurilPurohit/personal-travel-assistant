from calender_api.calender import calender
from flight_recommendations.flight import flight
from grok_api.extract_city import extract_city_from_text
import streamlit as st
import pandas as pd
import random
import re
from datetime import date, timedelta
from weather_module.weather import weather
import streamlit.components.v1 as components

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
    - **Total Price:** {flight['Price']}
    ---  
    ## 🏙 About {city}  
    - {history_points[0]}  
    - {history_points[1]}  
    - {history_points[2]}  
    🎉 Enjoy your trip!
    """

# Set up Streamlit page
st.set_page_config(page_title="Vacation Voyager", layout="wide")
st.title("✈ Vacation Voyager")
st.markdown("Plan your perfect trip in just a few clicks! 🚀")
st.markdown("👋 Welcome to Vacation Voyager! Let’s plan your dream trip together.")

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
    detected_city = extract_city_from_text(user_text)
    print(detected_city)
    # Always disable the dropdown when "Enter text" is selected, regardless of whether a city is detected
    dropdown_disabled = True
    
    if detected_city:
        city = detected_city
        st.sidebar.selectbox("Available destinations (disabled):", cities, 
                             index=cities.index(detected_city) if detected_city in cities else 0, 
                             disabled=dropdown_disabled)
    else:
        if user_text:
            st.sidebar.warning("No specific destination detected. Please try entering a city name more clearly.")
        city = None
        st.sidebar.selectbox("Available destinations (disabled):", cities, index=0, disabled=dropdown_disabled)
else:
    dropdown_disabled = False
    city = st.sidebar.selectbox("Select your destination:", cities, index=0, disabled=dropdown_disabled)
    print(city)

# Store the selected city
st.session_state.destination_city = city

passengers = st.sidebar.slider("Number of Passengers", 1, 10, 1)

trip_type = st.sidebar.radio("Trip Type", ["One way", "Round Trip"])

flight_class = st.sidebar.radio("Flight Class", ["Economy", "Premium Economy", "Business", "First Class"])

start_date = st.sidebar.date_input("Departure Date", date.today() + timedelta(days=1)) 
min_end_date = start_date + timedelta(days=1)
end_date = st.sidebar.date_input("Return Date", min_end_date, min_value=min_end_date, disabled=(trip_type == "One way"))

if trip_type == "One way":
    end_date = None  # Disable return date for One way

# Search Flights Button
if st.sidebar.button("🔍 Search Flights"):
    if city is None:
        st.sidebar.error("Please enter a valid destination or switch to dropdown selection.")
    else:
        st.session_state.destination_city = city
        
        # if city not in cities:
        #     st.sidebar.info(f"Searching for flights to {city}. This destination may have limited information available.")
        
        st.session_state.flights = flight("YYZ", city, start_date, end_date, passengers, trip_type, flight_class)
        st.session_state.selected_flight = None  # Reset selection on new search
        st.session_state.disable_selection = False  # Re-enable selection when searching again

# Show Available Flights After Search
if not st.session_state.flights.empty:
    st.subheader(f"⛅ Weather Forecast for {city}")
    weather_text = weather(city, start_date, end_date)
    weather_conditions = re.search(r"(sunny|cloudy|rainy|chilly)", weather_text.lower())
    if weather_conditions:
        condition = weather_conditions.group(0)
        icons = {"sunny": "☀️", "cloudy": "☁️", "rainy": "🌧️", "chilly": "❄️"}
        icon = icons.get(condition, "🌡️")
    else:
        icon = "🌡️"
    st.info(f"{weather_text} {icon}")

    # Travel tips based on city
    travel_tips = {
        "London": "Pack a light jacket for chilly mornings in March! Visit Buckingham Palace or a classic pub.",
        "Paris": "Bring comfortable shoes for exploring the Eiffel Tower and Louvre. Try a croissant at a local café!",
        "Tokyo": "Experience cherry blossoms if visiting in spring. Try sushi at a local spot in Shibuya.",
    }
    tip = travel_tips.get(city, f"Explore the local culture and attractions in {city}!")
    st.markdown(f"🌟 **Travel Tip:** {tip}")

    st.subheader("✈ Available Flights")
    df_flights = pd.DataFrame(st.session_state.flights)
    
    # Custom CSS for zebra striping and hover effects
    st.markdown(
        """
        <style>
        .stDataFrame {
            background-color: white;
        }
        .stDataFrame tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .stDataFrame tr:hover {
            background-color: #ddd;
            cursor: pointer;
        }
        .stDataFrame th {
            background-color: #4CAF50;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Display the dataframe
    st.dataframe(df_flights.style.set_properties(**{'text-align': 'center'}))

    # Flight Selection with Persistence
    st.subheader("📌 Select a Flight")
    flight_options = [
        f"{row['Airline']} | {row['Flight Number']} | {row['Price']}" for index, row in df_flights.iterrows()
    ]

    selected_flight_index = st.radio(
        "Choose your flight:", 
        list(range(len(flight_options))), 
        format_func=lambda x: flight_options[x], 
        index=None if st.session_state.selected_flight is None else flight_options.index(f"{st.session_state.selected_flight['Airline']} | {st.session_state.selected_flight['Flight Number']} | {st.session_state.selected_flight['Price']}"),
        disabled=st.session_state.disable_selection
    )

    if selected_flight_index is not None and not st.session_state.disable_selection:
        st.session_state.selected_flight = st.session_state.flights.iloc[selected_flight_index]
        st.session_state.disable_selection = True  # Lock selection after choosing a flight

else:
    print()

# Show Itinerary After Flight Selection
if st.session_state.selected_flight is not None:
    st.subheader("📝 Your Itinerary")
    st.success("Flight Selected! Generating Itinerary...")
    
    destination = st.session_state.destination_city
    st.info(f"Showing information for {destination}")
    
    with st.expander("View Itinerary Details"):
        st.markdown(generate_itinerary(st.session_state.selected_flight, destination), unsafe_allow_html=True)
    
    st.subheader("📅 Calendar Invite")
    # Custom button with confirmation modal
    components.html(
        """
        <div>
            <button id="downloadBtn" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
                📥 Download ICS
            </button>
            <div id="confirmModal" style="display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: white; padding: 20px; border: 1px solid #ccc; box-shadow: 0 0 10px rgba(0,0,0,0.5);">
                <h3>Confirm Download</h3>
                <p>Are you sure you want to download the calendar invite for your trip to {destination}?</p>
                <button onclick="document.getElementById('confirmModal').style.display='none'; document.getElementById('downloadLink').click();" style="background-color: #4CAF50; color: white; padding: 5px 10px; border: none; border-radius: 5px;">Yes</button>
                <button onclick="document.getElementById('confirmModal').style.display='none';" style="background-color: #f44336; color: white; padding: 5px 10px; margin-left: 10px; border: none; border-radius: 5px;">No</button>
            </div>
            <a id="downloadLink" href="{calender_link}" download="trip_to_{destination}.ics" style="display: none;">Download</a>
            <script>
                document.getElementById('downloadBtn').addEventListener('click', function() {{
                    document.getElementById('confirmModal').style.display = 'block';
                }});
            </script>
        </div>
        """.format(destination=destination, calender_link=calender(st.session_state.selected_flight)),
        height=100
    )
else:
    if st.session_state.selected_flight is None:
        st.warning("🔄 Not satisfied? Modify your search and try again!")