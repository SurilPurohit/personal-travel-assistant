from groq import Groq
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
import os
grok_api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=os.environ.get("grok_api_key"),
)

def city_suggestions(update_city):
    try:
        prompt = f'''
            Give 3 famous cities which are famous travel destinations around the world except {update_city} cities. Output should be return only updated city names.
            Please follow the examples given below.
            input -  give 3 famous cities
            output - Paris, New York, Toronto
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
        return summary

    except Exception as e:
        # Handle other potential errors
        print(f"An error occurred: {e}")