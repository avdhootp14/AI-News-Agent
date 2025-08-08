"""
AI News Agent - Main Entry Point
Daily AI news scraper, summarizer, and emailer using Gemini API
"""

import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from config_manager import ConfigManager
from logger_config import setup_logging
from orchestrator import NewsOrchestrator

def main():
    """Main entry point for the AI News Agent"""
    try:
        config = ConfigManager()

        logger = setup_logging(config)
        logger.info("Starting AI News Agent")

        orchestrator = NewsOrchestrator(config)
        orchestrator.run_daily_process()
        
        logger.info("AI News Agent completed successfully")
        
    except Exception as e:
        logging.error(f"Fatal error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()