import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.0-flash"
)


def understand_command(text):

    prompt = f"""
Convert this command into JSON.

Possible actions:
- open_website
- open_app
- google_search
- youtube_search
- type_text

User:
{text}

Only return JSON.
"""

    response = model.generate_content(prompt)

    try:

        data = json.loads(response.text)

        return data

    except:

        return {
            "action": "unknown"
        }