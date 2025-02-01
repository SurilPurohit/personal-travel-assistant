from groq import Groq
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
import os
grok_api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=os.environ.get("grok_api_key"),
)

def weather_summarize(user_city, start_date, end_date, weather_forecast):
    try:
        prompt = f'''
            Summarize the following weather forecast for {user_city} from {start_date} to {end_date} from the list of data {weather_forecast}. Highlight key trends, such as temperature ranges, how it feels, precipitation levels, and wind speed. Keep the summary concise, focusing on the overall weather pattern and notable observations. Also, suggest user whether it is optimal time to visit or not.
            Please follow the examples given below
            input - Weather forecast for Paris from 2025-02-02 to 2025-02-05:
                Date: 2025-02-02
                - Max Temp: 4.1°C
                - Min Temp: -0.8°C
                - Feels Like Max: 1.9°C
                - Feels Like Min: -3.6°C
                - Precipitation: 0.0 mm
                - Max Wind Speed: 4.7 km/h

                Date: 2025-02-03
                - Max Temp: 4.0°C
                - Min Temp: -0.2°C
                - Feels Like Max: 1.2°C
                - Feels Like Min: -3.3°C
                - Precipitation: 0.0 mm
                - Max Wind Speed: 7.3 km/h
            output - The weather forecast for Paris from February 2 to February 3, 2025, indicates cold conditions with maximum temperature of 4.1°C and a minimum temperature of -1.8°C. The "feels-like" temperatures are even lower, dropping as low as -5.1°C, making it feel much colder. No precipitation is expected throughout the period, ensuring dry conditions. Wind speeds remain moderate, peaking at 7.3 km/h on February 3. Overall, expect chilly, dry, and relatively calm weather with consistently cold mornings and cooler daytime highs.
        '''
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        summary = response.choices[0].message.content
        print(response.choices[0].message.content)
        return summary

    except Exception as e:
        # Handle other potential errors
        print(f"An error occurred: {e}")

    