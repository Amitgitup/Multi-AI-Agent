## Centralises all the model initialization

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config.settings import settings

def get_llm(model_name: str):

    try:
        if model_name.startswith("groq/"):
            model = model_name.split("/", 1)[1]

            return ChatGroq(
                model = model,
                groq_api_key = settings.GROQ_API_KEY
            )

        elif model_name.startswith("gemini/"):
            model = model_name.split("/", 1)[1]

            return ChatGoogleGenerativeAI(
                model = model,
                google_api_key = settings.GOOGLE_API_KEY
            )

    except Exception:
        return ChatGoogleGenerativeAI(
            model = "gemini-2.5-flash",
            google_api_key = settings.ALLOWED_MODEL_NAMES
        )