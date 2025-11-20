from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Autonomous QA Agent"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # LLM & Vector DB
    GROQ_API_KEY: str
    MILVUS_URI: str
    MILVUS_TOKEN: str
    
    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
