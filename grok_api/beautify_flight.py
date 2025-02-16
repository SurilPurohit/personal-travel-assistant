from groq import Groq
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
import os
grok_api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=os.environ.get("grok_api_key"),
)

def beautify_flight(flights_details, flight_type, price):
    try:
        prompt = f'''
            return the flight summary in a more readable and understandable form given below instead of {flights_details}, {flight_type}, {price}
        '''    
            # output should look like given below:
            #     Flight 1 details -
            #         - departure airport name with date and time
            #         - arrival airport name with date and time
            #         - round trip?
            #         - price
            #     Flight 2 details -
            #         - departure airport name with date and time
            #         - arrival airport name with date and time
            #         - round trip?
            #         - price
        
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
        # print(summary)
        return summary

    except Exception as e:
        # Handle other potential errors
        print(f"An error occurred: {e}")

    