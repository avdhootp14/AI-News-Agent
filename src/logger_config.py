"""Logging configuration for AI News Agent"""

import logging
import logging.handlers
import os
from pathlib import Path

def setup_logging(config_manager):
    """Setup logging configuration"""
    
    # Ensure logs directory exists
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Get logging configuration
    log_level = config_manager.get('logging.level', 'INFO')
    log_file = config_manager.get('logging.file', 'logs/ai_news_agent.log')
    log_format = config_manager.get('logging.format', 
                                   '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    max_size = config_manager.get('logging.max_size', '10MB')
    backup_count = config_manager.get('logging.backup_count', 5)
    
    # Convert max_size string to bytes
    if isinstance(max_size, str):
        if max_size.endswith('MB'):
            max_bytes = int(max_size[:-2]) * 1024 * 1024
        elif max_size.endswith('KB'):
            max_bytes = int(max_size[:-2]) * 1024
        else:
            max_bytes = int(max_size)
    else:
        max_bytes = max_size
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=[
            # File handler with rotation
            logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count
            ),
            # Console handler
            logging.StreamHandler()
        ]
    )
    
    # Set up specific loggers
    logger = logging.getLogger('ai_news_agent')
    logger.info("Logging system initialized")
    
    return logger
