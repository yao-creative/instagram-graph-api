import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Instagram Graph API Service"
    DEBUG: bool = False
    
    # Instagram API Configuration
    INSTAGRAM_API_VERSION: str = "v22.0"
    INSTAGRAM_API_BASE_URL: str = "https://graph.instagram.com"
    INSTAGRAM_ACCESS_TOKEN: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings object
settings = Settings() 