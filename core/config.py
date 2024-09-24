import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    MONGO_URI: str
    DATABASE_NAME: str

settings = Settings()