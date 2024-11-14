import os

import google.generativeai as genai

from app.config.database import db

genai.configure(api_key=os.environ["API_KEY"])


async def summarize_transcription(text: str):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(text)
    return response.text
