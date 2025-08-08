"""Main orchestrator for AI News Agent"""

import logging
from typing import List, Dict
from datetime import datetime

from scrappers.news_scraper import NewsScraper
from summarizer.gemini_summarizer import GeminiSummarizer
from email_system.email_sender import EmailSender
from email_system.email_formatter import EmailFormatter

class NewsOrchestrator:
    """Orchestrates the daily news process"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger('ai_news_agent.orchestrator')       
        self.scraper = NewsScraper(config_manager)
        self.summarizer = GeminiSummarizer(config_manager)
        self.email_formatter = EmailFormatter(config_manager)
        self.email_sender = EmailSender(config_manager)
    
    def run_daily_process(self):
        """Run the complete daily news process"""
        try:
            self.logger.info("Starting daily news process")
            
            # Step 1: Scrape news articles
            articles = self.scrape_articles()
            if not articles:
                self.logger.warning("No articles found. Skipping email.")
                return
            
            # Step 2: Summarize articles using Gemini
            summarized_articles = self.summarize_articles(articles)
            
            # Step 3: Format email
            email_content = self.email_formatter.format_email(summarized_articles)
            
            # Step 4: Send email
            self.email_sender.send_email(email_content)
            
            self.logger.info(f"Daily process completed successfully. Processed {len(summarized_articles)} articles.")
            
        except Exception as e:
            self.logger.error(f"Error in daily process: {e}")
            raise
    
    def scrape_articles(self) -> List[Dict]:
        """Scrape articles from configured news sources"""
        try:
            self.logger.info("Starting article scraping")
            articles = self.scraper.scrape_all_sources()
            self.logger.info(f"Scraped {len(articles)} articles")
            return articles
            
        except Exception as e:
            self.logger.error(f"Error scraping articles: {e}")
            return []
    
    def summarize_articles(self, articles: List[Dict]) -> List[Dict]:
        """Summarize articles using Gemini API"""
        try:
            self.logger.info(f"Starting summarization for {len(articles)} articles")
            summarized = []
            
            for article in articles:
                try:
                    summary = self.summarizer.summarize(article.get('content', ''))
                    article['ai_summary'] = summary
                    summarized.append(article)
                    self.logger.debug(f"Summarized article: {article.get('title', 'Unknown')}")
                    
                except Exception as e:
                    self.logger.warning(f"Failed to summarize article '{article.get('title', 'Unknown')}': {e}")
                    # Use fallback - original summary or first paragraph
                    article['ai_summary'] = article.get('summary', article.get('content', '')[:200] + '...')
                    summarized.append(article)
            
            self.logger.info(f"Summarization completed. {len(summarized)} articles processed.")
            return summarized
            
        except Exception as e:
            self.logger.error(f"Error in summarization process: {e}")
            return articles  # Return original articles as fallback
