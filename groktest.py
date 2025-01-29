from groq import Groq
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
import os
grok_api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=os.environ.get("grok_api_key"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama-3.1-8b-instant",
)

print(chat_completion.choices[0].message.content)