from typing import Any, Dict, List, Optional
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Instagram Graph API Service"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Any) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Instagram API Configuration
    INSTAGRAM_API_VERSION: str = "v22.0"
    INSTAGRAM_API_BASE_URL: str = "https://graph.instagram.com"
    INSTAGRAM_ACCESS_TOKEN: Optional[str] = None
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    
    # Supabase Configuration
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    SUPABASE_TABLE_NAME: str = "instagram_data"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create global settings object
settings = Settings() 