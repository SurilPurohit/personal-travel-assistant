from groq import Groq
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
import os
grok_api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=os.environ.get("grok_api_key"),
)

def generate_itinerary(flight, city, weather_conditions):
    try:
        prompt = f'''
            Generate a travel itinerary with the following details:
            {flight} and {weather_conditions}
            Provide a short description of {city}, including notable landmarks, the city's significance, and its cultural or historical importance. Also, add a fun, one-line travel tip at the end.

            Format the response like the following example, using emojis and a clear structure:

            🌍 **Your Itinerary**  
            ✈️ **Airline**: Air Canada  
            🛫 **Flight Number**: AC 858  
            💰 **Total Price**: 728  

            🏙 **About London**  
            Capital of England and the United Kingdom. Home to Buckingham Palace and the Tower of London. Known for its rich history and diverse culture.  

            🎉 **Travel Tip**: Don’t forget to pack an umbrella in London, it’s known for its sudden showers!  

            🎒 **Enjoy your trip!**

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
        # print(response.choices[0].message.content)
        # print(summary)
        return summary

    except Exception as e:
        # Handle other potential errors
        print(f"An error occurred: {e}")