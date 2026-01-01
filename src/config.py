"""
Configuration and environment handling for LinkedIn Profile Optimization Agent
Cloud-optimized for Streamlit Community Cloud deployment
"""

import os
import tempfile
from typing import Optional

# Load .env only for local development (never in production)
if os.path.exists(".env") and not os.getenv("STREAMLIT_CLOUD"):
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # dotenv not available, continue without it

class Config:
    """Configuration class for the application"""
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    TOGETHER_API_KEY: str = os.getenv("TOGETHER_API_KEY", "")
    
    # Langfuse Configuration (Optional)
    LANGFUSE_SECRET_KEY: Optional[str] = os.getenv("LANGFUSE_SECRET_KEY")
    LANGFUSE_PUBLIC_KEY: Optional[str] = os.getenv("LANGFUSE_PUBLIC_KEY")
    LANGFUSE_HOST: Optional[str] = os.getenv("LANGFUSE_HOST")
    
    # Model Configuration
    CUSTOM_LLAMA3_MODEL_ID: Optional[str] = os.getenv("CUSTOM_LLAMA3_MODEL_ID")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gpt4o")
    
    # App Configuration
    MAX_IMAGE_WIDTH: int = int(os.getenv("MAX_IMAGE_WIDTH", "1024"))
    
    # File Paths - Cloud-friendly with temporary directory fallbacks
    TRAINING_DATA_PATH: str = os.getenv("TRAINING_DATA_PATH", os.path.join(tempfile.gettempdir(), "training_dataset.jsonl"))
    LOGS_PATH: str = os.getenv("LOGS_PATH", os.path.join(tempfile.gettempdir(), "telemetry_logs.json"))
    TEMP_DIR: str = tempfile.gettempdir()
    
    # Model IDs
    GPT4O_MODEL_ID: str = "gpt-4o"
    GPT4O_VISION_MODEL_ID: str = "gpt-4o"
    LLAMA3_BASE_MODEL: str = "meta-llama-3-8b-instruct"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
        return True
    
    @classmethod
    def is_langfuse_configured(cls) -> bool:
        """Check if Langfuse is properly configured"""
        return all([cls.LANGFUSE_SECRET_KEY, cls.LANGFUSE_PUBLIC_KEY, cls.LANGFUSE_HOST])
    
    @classmethod
    def is_together_configured(cls) -> bool:
        """Check if Together AI is properly configured"""
        return bool(cls.TOGETHER_API_KEY)
    
    @classmethod
    def has_custom_llama3(cls) -> bool:
        """Check if a custom Llama 3 model is available"""
        return bool(cls.CUSTOM_LLAMA3_MODEL_ID)
    
    @classmethod
    def get_env_status(cls) -> dict:
        """Get status of environment variables for cloud deployment UI"""
        return {
            "OPENAI_API_KEY": bool(cls.OPENAI_API_KEY),
            "TOGETHER_API_KEY": bool(cls.TOGETHER_API_KEY),
            "LANGFUSE_CONFIGURED": cls.is_langfuse_configured(),
            "CUSTOM_MODEL_AVAILABLE": cls.has_custom_llama3(),
            "TRAINING_DATA_PATH": cls.TRAINING_DATA_PATH,
            "IS_CLOUD_DEPLOYMENT": bool(os.getenv("STREAMLIT_CLOUD"))
        }
