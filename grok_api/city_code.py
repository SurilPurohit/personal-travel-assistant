from groq import Groq
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
import os
grok_api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=os.environ.get("grok_api_key"),
)

def city_code(city):
    try:
        prompt = f'''
            Just return the IATA code for the most famous airport in {city}. No extra text.
            For example:
            Input: Mumbai
            Output: BOM
            Input: London
            Output: LHR

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
        # print(summary)
        return summary

    except Exception as e:
        # Handle other potential errors
        print(f"An error occurred: {e}")

    