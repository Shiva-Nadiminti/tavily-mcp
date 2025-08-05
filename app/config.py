from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    tavily_api_key: Optional[str] = None  # Make optional for development
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    debug: bool = False

    class Config:
        env_file = ".env.example"
        extra = "ignore"  # Ignore extra env variables

settings = Settings()

# Add validation check
if settings.tavily_api_key is None:
    raise ValueError("TAVILY_API_KEY is required in .env file")