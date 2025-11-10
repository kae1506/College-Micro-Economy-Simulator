from google import genai
from google.genai import types
from google.genai.errors import APIError

try:
    import os
    from dotenv import load_dotenv

    load_dotenv()

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    print(os.getenv("GEMINI_API_KEY"))
except Exception as e:
    print("Error initializing Gemini client:")
    print("Ensure GEMINI_API_KEY environment variable is set.")
    print(e)
    exit()
