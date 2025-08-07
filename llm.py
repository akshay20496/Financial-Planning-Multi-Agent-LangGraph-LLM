from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
gemini_api_key = os.getenv("gemini_key")

class LLM:
    def __init__(self, model_name, temperature):
        self.model_name = model_name
        self.temperature = temperature

    def get_model(self):
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature,
            api_key=gemini_api_key,
            top_p=0.95,
            top_k=40,
        )
