import os
from typing import Optional
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # App
    APP_NAME: str = "NEXUS-INTEL"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database
    DATABASE_URL: str = Field("sqlite:///./nexus.db", env="DATABASE_URL")
    NEO4J_URL: str = Field("bolt://localhost:7687", env="NEO4J_URL")
    NEO4J_USER: str = Field("neo4j", env="NEO4J_USER")
    NEO4J_PASSWORD: str = Field("password", env="NEO4J_PASSWORD")
    REDIS_URL: str = Field("redis://localhost:6379", env="REDIS_URL")
    
    # AI/ML
    OPENAI_API_KEY: Optional[str] = Field(None, env="OPENAI_API_KEY")
    HF_TOKEN: Optional[str] = Field(None, env="HF_TOKEN")
    
    # Multi-language
    SUPPORTED_LANGUAGES: list = ["en", "hi", "ta", "te", "bn"]
    DEFAULT_LANGUAGE: str = "en"
    
    # Offline mode
    OFFLINE_MODE: bool = False
    SYNC_INTERVAL: int = 300  # 5 minutes
    
    # Security
    ENCRYPTION_KEY: str = Field(..., env="ENCRYPTION_KEY")
    ROLE_BASED_ACCESS: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()