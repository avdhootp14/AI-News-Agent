"""News scraper for AI News Agent"""

import requests
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


class NewsScraper:
    """Scrapes news articles from configured sources"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger('ai_news_agent.scraper')
        
        # Get scraping configuration
        scraping_config = self.config.get_scraping_config()
        self.rate_limit_delay = scraping_config.get('rate_limit_delay', 2)
        self.max_articles = scraping_config.get('max_articles', 5)
        self.hours_lookback = scraping_config.get('hours_lookback', 24)
        self.user_agent = scraping_config.get('user_agent', 'AI-News-Agent/1.0')
        self.timeout = scraping_config.get('timeout', 30)
        
        # Setup session with headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def scrape_all_sources(self) -> List[Dict]:
        """Scrape articles from all configured news sources"""
        all_articles = []
        sources = self.config.get_news_sources()
        
        self.logger.info(f"Scraping {len(sources)} news sources")
        
        for source in sources:
            try:
                self.logger.info(f"Scraping {source['name']}: {source['url']}")
                articles = self.scrape_source(source)
                all_articles.extend(articles)
                
                # Rate limiting between sources
                time.sleep(self.rate_limit_delay)
                
            except Exception as e:
                self.logger.error(f"Error scraping {source['name']}: {e}")
                continue
        
        # Sort by date and limit to max_articles
        all_articles.sort(key=lambda x: x.get('published_date', datetime.min), reverse=True)
        limited_articles = all_articles[:self.max_articles]
        
        self.logger.info(f"Total articles collected: {len(limited_articles)}")
        return limited_articles
    
    def scrape_source(self, source: Dict) -> List[Dict]:
        """Scrape articles from a single news source"""
        url = source['url']
        source_name = source['name']
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Route to specific scraper based on domain
            domain = urlparse(url).netloc
            
            if 'artificialintelligence-news.com' in domain:
                return self._scrape_ai_news(soup, source_name, url)
            elif 'theverge.com' in domain:
                return self._scrape_verge(soup, source_name, url)
            elif 'techcrunch.com' in domain:
                return self._scrape_techcrunch(soup, source_name, url)
            else:
                return self._scrape_generic(soup, source_name, url)
                
        except requests.RequestException as e:
            self.logger.error(f"Network error scraping {source_name}: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Error parsing {source_name}: {e}")
            return []
    
    def _scrape_ai_news(self, soup: BeautifulSoup, source_name: str, base_url: str) -> List[Dict]:
        """Scrape articles from artificialintelligence-news.com"""
        articles = []
        
        # Find article containers (this may need adjustment based on actual site structure)
        article_elements = soup.find_all(['article', 'div'], class_=lambda x: x and any(
            keyword in x.lower() for keyword in ['post', 'article', 'news', 'item']
        ))[:10]  # Limit to first 10 for performance
        
        for element in article_elements:
            try:
                article = self._extract_article_data(element, source_name, base_url)
                if article and self._is_recent_article(article.get('published_date')):
                    articles.append(article)
            except Exception as e:
                self.logger.debug(f"Error extracting article from AI News: {e}")
                continue
        
        return articles
    
    def _scrape_verge(self, soup: BeautifulSoup, source_name: str, base_url: str) -> List[Dict]:
        """Scrape articles from The Verge AI section"""
        articles = []
        
        # Find article containers
        article_elements = soup.find_all(['article', 'div'], class_=lambda x: x and any(
            keyword in x.lower() for keyword in ['duet', 'entry', 'article', 'story']
        ))[:10]
        
        for element in article_elements:
            try:
                article = self._extract_article_data(element, source_name, base_url)
                if article and self._is_recent_article(article.get('published_date')):
                    articles.append(article)
            except Exception as e:
                self.logger.debug(f"Error extracting article from The Verge: {e}")
                continue
        
        return articles
    
    def _scrape_techcrunch(self, soup: BeautifulSoup, source_name: str, base_url: str) -> List[Dict]:
        """Scrape articles from TechCrunch AI section"""
        articles = []
        
        # Find article containers
        article_elements = soup.find_all(['article', 'div'], class_=lambda x: x and any(
            keyword in x.lower() for keyword in ['post', 'article', 'entry']
        ))[:10]
        
        for element in article_elements:
            try:
                article = self._extract_article_data(element, source_name, base_url)
                if article and self._is_recent_article(article.get('published_date')):
                    articles.append(article)
            except Exception as e:
                self.logger.debug(f"Error extracting article from TechCrunch: {e}")
                continue
        
        return articles
    
    def _scrape_generic(self, soup: BeautifulSoup, source_name: str, base_url: str) -> List[Dict]:
        """Generic scraper for unknown news sources"""
        articles = []
        
        # Look for common article patterns
        article_elements = soup.find_all(['article', 'div'], limit=15)
        
        for element in article_elements:
            try:
                article = self._extract_article_data(element, source_name, base_url)
                if article and self._is_recent_article(article.get('published_date')):
                    articles.append(article)
            except Exception as e:
                self.logger.debug(f"Error extracting article from {source_name}: {e}")
                continue
        
        return articles
    
    def _extract_article_data(self, element, source_name: str, base_url: str) -> Dict:
        """Extract article data from a BeautifulSoup element"""
        
        # Find title
        title_element = element.find(['h1', 'h2', 'h3', 'h4', 'a'], class_=lambda x: x and any(
            keyword in x.lower() for keyword in ['title', 'headline', 'head']
        ))
        
        if not title_element:
            title_element = element.find(['h1', 'h2', 'h3', 'h4'])
        
        if not title_element:
            title_element = element.find('a')
        
        if not title_element:
            return None
        
        title = title_element.get_text(strip=True)
        if not title or len(title) < 10:  # Skip if title too short
            return None
        
        # Find URL
        url_element = title_element if title_element.name == 'a' else title_element.find('a')
        if not url_element:
            url_element = element.find('a')
        
        article_url = ""
        if url_element and url_element.get('href'):
            href = url_element.get('href')
            article_url = urljoin(base_url, href)
        
        # Find summary/content
        summary_element = element.find(['p', 'div'], class_=lambda x: x and any(
            keyword in x.lower() for keyword in ['summary', 'excerpt', 'description', 'content']
        ))
        
        if not summary_element:
            summary_element = element.find('p')
        
        summary = ""
        if summary_element:
            summary = summary_element.get_text(strip=True)
        
        # Find date
        date_element = element.find(['time', 'span', 'div'], class_=lambda x: x and any(
            keyword in x.lower() for keyword in ['date', 'time', 'published']
        ))
        
        published_date = datetime.now()  # Default to now
        if date_element:
            date_text = date_element.get('datetime') or date_element.get_text(strip=True)
            published_date = self._parse_date(date_text)
        
        return {
            'title': title,
            'url': article_url,
            'summary': summary,
            'content': summary,  # For now, use summary as content
            'published_date': published_date,
            'source': source_name
        }
    
    def _parse_date(self, date_text: str) -> datetime:
        """Parse date from various string formats"""
        try:
            # Try common date formats
            formats = [
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d',
                '%B %d, %Y',
                '%b %d, %Y',
                '%d %B %Y',
                '%d %b %Y'
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_text[:19], fmt)
                except ValueError:
                    continue
            
            # If no format matches, return current time
            return datetime.now()
            
        except Exception:
            return datetime.now()
    
    def _is_recent_article(self, published_date: datetime) -> bool:
        """Check if article is within the lookback period"""
        if not published_date:
            return True  # Include if no date available
        
        cutoff_date = datetime.now() - timedelta(hours=self.hours_lookback)
        return published_date >= cutoff_date