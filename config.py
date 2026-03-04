"""
Configuration management with validation and environment support.
Prevents NameError by ensuring all configuration variables are properly defined.
"""
import os
from pathlib import Path
from typing import Optional
from pydantic import BaseSettings, Field, validator
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

class MissionConfig(BaseSettings):
    """Validated configuration for CERBERUS GATE mission."""
    
    # Mission parameters
    mission_id: str = Field(default="CERBERUS_GATE_001", env="MISSION_ID")
    max_retries: int = Field(default=3, ge=1, le=10, env="MAX_RETRIES")
    timeout_seconds: int = Field(default=30, ge=5, le=300, env="TIMEOUT_SECONDS")
    
    # AI Model configuration
    model_provider: str = Field(default="deepseek", env="MODEL_PROVIDER")
    fallback_models: list = Field(default=["openai", "anthropic", "local"], env="FALLBACK_MODELS")
    
    # Firebase configuration (CRITICAL for state management)
    firebase_project_id: Optional[str] = Field(env="FIREBASE_PROJECT_ID")
    firebase_credentials_path: Optional[str] = Field(env="FIREBASE_CREDENTIALS_PATH")
    
    # Telegram alerting
    telegram_bot_token: Optional[str] = Field(env="TELEGRAM_BOT_TOKEN")
    telegram_chat_id: Optional[str] = Field(env="TELEGRAM_CHAT_ID")
    
    # Logging configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    enable_telemetry: bool = Field(default=True, env="ENABLE_TELEMETRY")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @validator('firebase_project_id', pre=True)
    def validate_firebase_config(cls, v):
        """Validate Firebase configuration exists."""
        if not v:
            raise ValueError("Firebase project ID is required for state management")
        return v

# Global configuration instance - prevents NameError
CONFIG = MissionConfig