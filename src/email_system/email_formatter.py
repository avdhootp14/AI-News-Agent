"""Email formatting for AI News Agent"""

import logging
from datetime import datetime
from typing import List, Dict


class EmailFormatter:
    """Formats news articles into professional HTML emails"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger('ai_news_agent.email_formatter')
        
        # Get email configuration
        email_config = self.config.get_email_config()
        template_config = email_config.get('template', {})
        self.subject_prefix = template_config.get('subject_prefix', 'Daily AI News Digest')
        self.sender_name = template_config.get('sender_name', 'AI News Agent')
    
    def format_email(self, articles: List[Dict]) -> Dict[str, str]:
        """
        Format articles into email content
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            Dictionary with 'subject', 'html_body', and 'text_body'
        """
        try:
            current_date = datetime.now().strftime("%B %d, %Y")
            
            # Create subject
            subject = f"{self.subject_prefix} – {current_date}"
            
            # Create HTML body
            html_body = self._create_html_body(articles, current_date)
            
            # Create plain text body
            text_body = self._create_text_body(articles, current_date)
            
            self.logger.info(f"Email formatted successfully with {len(articles)} articles")
            
            return {
                'subject': subject,
                'html_body': html_body,
                'text_body': text_body
            }
            
        except Exception as e:
            self.logger.error(f"Error formatting email: {e}")
            raise
    
    def _create_html_body(self, articles: List[Dict], date: str) -> str:
        """Create HTML email body"""
        
        # HTML template
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily AI News Digest</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #007acc;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #007acc;
            margin: 0;
            font-size: 28px;
        }}
        .date {{
            color: #666;
            font-size: 16px;
            margin-top: 5px;
        }}
        .intro {{
            font-size: 16px;
            margin-bottom: 30px;
            color: #555;
        }}
        .article {{
            margin-bottom: 30px;
            padding-bottom: 25px;
            border-bottom: 1px solid #eee;
        }}
        .article:last-child {{
            border-bottom: none;
            margin-bottom: 0;
        }}
        .article-title {{
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .article-title a {{
            color: #007acc;
            text-decoration: none;
        }}
        .article-title a:hover {{
            text-decoration: underline;
        }}
        .article-meta {{
            font-size: 14px;
            color: #888;
            margin-bottom: 12px;
        }}
        .article-summary {{
            font-size: 16px;
            line-height: 1.7;
            color: #444;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            text-align: center;
            color: #666;
            font-size: 14px;
        }}
        .unsubscribe {{
            margin-top: 15px;
            font-size: 12px;
        }}
        .unsubscribe a {{
            color: #888;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Daily AI News Digest</h1>
            <div class="date">{date}</div>
        </div>
        
        <div class="intro">
            Hello AI Enthusiast! Here's your daily roundup of the latest AI news and developments.
        </div>
        
        <div class="articles">
{self._format_articles_html(articles)}
        </div>
        
        <div class="footer">
            <p>Stay informed and ahead of the curve!</p>
            <p><strong>{self.sender_name}</strong></p>
            <div class="unsubscribe">
                <a href="mailto:unsubscribe@example.com?subject=Unsubscribe">Unsubscribe</a> from this newsletter
            </div>
        </div>
    </div>
</body>
</html>
"""
        return html_template
    
    def _format_articles_html(self, articles: List[Dict]) -> str:
        """Format articles as HTML"""
        articles_html = ""
        
        for i, article in enumerate(articles, 1):
            title = article.get('title', 'Untitled Article')
            url = article.get('url', '#')
            summary = article.get('ai_summary', article.get('summary', 'No summary available'))
            source = article.get('source', 'Unknown Source')
            date = article.get('published_date', datetime.now())
            
            # Format date
            if isinstance(date, datetime):
                formatted_date = date.strftime("%B %d, %Y")
            else:
                formatted_date = "Recent"
            
            article_html = f"""
            <div class="article">
                <div class="article-title">
                    <a href="{url}" target="_blank">{title}</a>
                </div>
                <div class="article-meta">
                    {source} • {formatted_date}
                </div>
                <div class="article-summary">
                    {summary}
                </div>
            </div>
"""
            articles_html += article_html
        
        return articles_html
    
    def _create_text_body(self, articles: List[Dict], date: str) -> str:
        """Create plain text email body"""
        
        text_body = f"""
DAILY AI NEWS DIGEST - {date}

Hello AI Enthusiast!

Here's your daily roundup of the latest AI news and developments:

"""
        
        for i, article in enumerate(articles, 1):
            title = article.get('title', 'Untitled Article')
            url = article.get('url', '')
            summary = article.get('ai_summary', article.get('summary', 'No summary available'))
            source = article.get('source', 'Unknown Source')
            date = article.get('published_date', datetime.now())
            
            # Format date
            if isinstance(date, datetime):
                formatted_date = date.strftime("%B %d, %Y")
            else:
                formatted_date = "Recent"
            
            text_body += f"""
{i}. {title}
   Source: {source} | {formatted_date}
   
   {summary}
   
   Read more: {url}

{'='*60}

"""
        
        text_body += f"""

Stay informed and ahead of the curve!

{self.sender_name}

---
To unsubscribe, reply with "UNSUBSCRIBE" in the subject line.
"""
        
        return text_body
