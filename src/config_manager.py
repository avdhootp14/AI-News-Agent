"""Configuration management for AI News Agent"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        # Load environment variables
        load_dotenv()
        
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
        """Load sensitive data from environment variables"""
        # Gemini API key
        gemini_key = os.getenv('GEMINI_API_KEY')
        if gemini_key:
            if 'gemini' not in self.config:
                self.config['gemini'] = {}
            self.config['gemini']['api_key'] = gemini_key
        
        # Email credentials
        email_username = os.getenv('EMAIL_USERNAME')
        email_password = os.getenv('EMAIL_PASSWORD')
        
        if email_username and email_password:
            if 'email' not in self.config:
                self.config['email'] = {}
            if 'credentials' not in self.config['email']:
                self.config['email']['credentials'] = {}
            
            self.config['email']['credentials']['username'] = email_username
            self.config['email']['credentials']['password'] = email_password
    
    def get(self, key: str, default=None):
        """Get configuration value by key"""
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
