# backend/app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Contract Intelligence"
    API_V1_STR: str = "/api/v1"
    MONGO_URI: str
    MONGO_DB_NAME: str
    MONGO_COLLECTION: str  # ✅ add this

    class Config:
        env_file = ".env"
        extra = "ignore"  # avoids errors if extra vars exist


settings = Settings()