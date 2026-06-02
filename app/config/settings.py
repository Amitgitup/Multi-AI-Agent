from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

    ALLOWED_MODEL_NAMES = ["groq/llama-3.3-70b-versatile", "groq/llama-3.1-8b-instant", "gemini/gemini-2.5-flash", "gemini/gemini-2.5-pro"]

settings = Settings()