import os
import json
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

class SingleUserConfig(BaseModel):
    """Configuration for the single user system."""
    name: str
    email: EmailStr
    password: str
    avatar: Optional[str] = None
    plan: str = "premium"

class AppConfig:
    """Application configuration manager."""
    
    def __init__(self):
        self.data_dir = Path(os.environ.get("DATA_DIR", "data"))
        self.config_file = self.data_dir / "config.json"
        self.data_dir.mkdir(exist_ok=True)
        
        # JWT Settings
        self.jwt_secret_key = os.environ.get("JWT_SECRET_KEY", "your-secret-key-change-in-production")
        self.jwt_algorithm = "HS256"
        self.jwt_expire_minutes = 30 * 24 * 60  # 30 days
        
        # API Settings
        self.api_key_length = 32
        self.max_api_keys = 10
        
        # Single user configuration
        self.user_config = self._load_user_config()
    
    def _load_user_config(self) -> Optional[SingleUserConfig]:
        """Load user configuration from environment or config file."""
        
        # Try environment variables first
        env_name = os.environ.get("BLOTATO_USER_NAME")
        env_email = os.environ.get("BLOTATO_USER_EMAIL")
        env_password = os.environ.get("BLOTATO_USER_PASSWORD")
        
        if env_name and env_email and env_password:
            return SingleUserConfig(
                name=env_name,
                email=env_email,
                password=env_password,
                avatar=os.environ.get("BLOTATO_USER_AVATAR"),
                plan=os.environ.get("BLOTATO_USER_PLAN", "premium")
            )
        
        # Try config file
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    return SingleUserConfig(**config_data.get("user", {}))
            except (json.JSONDecodeError, KeyError, ValueError):
                pass
        
        return None
    
    def save_user_config(self, user_config: SingleUserConfig):
        """Save user configuration to config file."""
        config_data = {"user": user_config.dict()}
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        self.user_config = user_config
    
    def is_configured(self) -> bool:
        """Check if the system is configured with a user."""
        return self.user_config is not None
    
    def get_user_id(self) -> str:
        """Get the single user ID."""
        return "single-user"
    
    def validate_user_credentials(self, email: str, password: str) -> bool:
        """Validate user credentials."""
        if not self.user_config:
            return False
        
        return (self.user_config.email == email and 
                self.user_config.password == password)

# Global configuration instance
config = AppConfig()

def get_config() -> AppConfig:
    """Get the global configuration instance."""
    return config

def setup_initial_user(name: str, email: str, password: str, avatar: str = None) -> bool:
    """Setup the initial user if not already configured."""
    if config.is_configured():
        return False
    
    user_config = SingleUserConfig(
        name=name,
        email=email,
        password=password,
        avatar=avatar or f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=6366f1&color=fff",
        plan="premium"
    )
    
    config.save_user_config(user_config)
    return True

def get_user_data() -> Optional[dict]:
    """Get the single user data."""
    if not config.user_config:
        return None
    
    return {
        "_id": config.get_user_id(),
        "name": config.user_config.name,
        "email": config.user_config.email,
        "avatar": config.user_config.avatar,
        "plan": config.user_config.plan,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
