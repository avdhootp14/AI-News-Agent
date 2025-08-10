"""Configuration management for AI News Agent"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv


class ConfigManager:
    """Manages application configuration"""

    def __init__(self, config_path: str = "config/config.yaml"):
        # Load local .env if available (for local dev)
        env_path = Path(__file__).parent.parent / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
        else:
            load_dotenv()  # fallback to current dir

        self.config_path = config_path
        self.config = self._load_config()
        self._load_env_variables()

    def _load_config(self) -> Dict[Any, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML configuration: {e}")

    def _load_env_variables(self):
        """Load sensitive data from environment variables (overrides YAML values)"""

        # Gemini API key
        self.config.setdefault('gemini', {})['api_key'] = os.getenv(
            'GEMINI_API_KEY',
            self.config.get('gemini', {}).get('api_key')
        )

        # Email credentials
        self.config.setdefault('email', {}).setdefault('credentials', {})
        self.config['email']['credentials']['username'] = os.getenv(
            'EMAIL_USERNAME',
            self.config['email']['credentials'].get('username')
        )
        self.config['email']['credentials']['password'] = os.getenv(
            'EMAIL_PASSWORD',
            self.config['email']['credentials'].get('password')
        )

        # SendGrid API key
        self.config.setdefault('sendgrid', {})['api_key'] = os.getenv(
            'SENDGRID_API_KEY',
            self.config.get('sendgrid', {}).get('api_key')
        )

        # News API key
        self.config.setdefault('news_api', {})['api_key'] = os.getenv(
            'NEWS_API_KEY',
            self.config.get('news_api', {}).get('api_key')
        )

    def get(self, key: str, default=None):
        """Get configuration value by key, e.g., 'gemini.api_key'"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
            if value is None:
                return default
        return value

    def get_news_sources(self):
        """Get enabled news sources"""
        sources = self.get('news_sources', [])
        return [source for source in sources if source.get('enabled', True)]

    def get_gemini_config(self):
        """Get Gemini API configuration"""
        return self.get('gemini', {})

    def get_email_config(self):
        """Get email configuration"""
        return self.get('email', {})

    def get_scraping_config(self):
        """Get scraping configuration"""
        return self.get('scraping', {})

