from groq import Groq
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
import os
grok_api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=os.environ.get("grok_api_key"),
)

def extract_city_from_text(user_text):
    try:
        prompt = f'''
            Extract the name of the city from the following text:
            Input: {user_text}
            Output: Only the name of the city, no other text.
            For example:
            Input: I want to travel to Tokyo next week
            Output: Tokyo

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