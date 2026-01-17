# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    # We are using the bleeding-edge model you have access to!
    MODEL_NAME = "gemini-flash-latest" 

settings = Settings()