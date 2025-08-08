"""Gemini API summarizer for AI News Agent"""

import logging
import time
import google.generativeai as genai
from typing import Optional


class GeminiSummarizer:
    """Summarizes articles using Google's Gemini API"""
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger('ai_news_agent.summarizer')
        
        # Get Gemini configuration
        gemini_config = self.config.get_gemini_config()
        self.model_name = gemini_config.get('model', 'gemini-pro')
        self.max_tokens = gemini_config.get('max_tokens', 150)
        self.temperature = gemini_config.get('temperature', 0.3)
        self.retry_attempts = gemini_config.get('retry_attempts', 3)
        self.retry_delay = gemini_config.get('retry_delay', 5)
        
        # Initialize Gemini API
        self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Initialize Gemini API client"""
        try:
            api_key = self.config.get('gemini.api_key')
            if not api_key:
                raise ValueError("Gemini API key not found in configuration")
            
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(self.model_name)
            
            self.logger.info(f"Gemini API initialized with model: {self.model_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini API: {e}")
            raise
    
    def summarize(self, content: str) -> str:
        """
        Summarize article content using Gemini API
        
        Args:
            content: Article content to summarize
            
        Returns:
            Summarized content string
        """
        if not content or len(content.strip()) < 50:
            self.logger.warning("Content too short for summarization")
            return content
        
        prompt = self._create_prompt(content)
        
        for attempt in range(self.retry_attempts):
            try:
                self.logger.debug(f"Summarization attempt {attempt + 1}/{self.retry_attempts}")
                
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=self.max_tokens,
                        temperature=self.temperature,
                    )
                )
                
                if response.text:
                    summary = response.text.strip()
                    self.logger.debug("Summarization successful")
                    return summary
                else:
                    self.logger.warning("Empty response from Gemini API")
                    
            except Exception as e:
                self.logger.warning(f"Summarization attempt {attempt + 1} failed: {e}")
                
                if attempt < self.retry_attempts - 1:
                    time.sleep(self.retry_delay)
                else:
                    self.logger.error("All summarization attempts failed")
                    raise
        
        # If we get here, all attempts failed
        return self._create_fallback_summary(content)
    
    def _create_prompt(self, content: str) -> str:
        """Create a prompt for Gemini API"""
        prompt = f"""
        Please summarize the following AI-related news article in 50-100 words. 
        Focus on the main points and maintain a professional tone. 
        Make the summary engaging and informative for someone interested in AI developments.
        
        Article content:
        {content[:2000]}  # Limit content length to avoid token limits
        
        Summary:
        """
        return prompt
    
    def _create_fallback_summary(self, content: str) -> str:
        """Create a fallback summary when API fails"""
        self.logger.info("Creating fallback summary")
        
        # Simple extractive summarization - take first few sentences
        sentences = content.split('. ')
        
        # Take first 2-3 sentences, up to ~100 words
        summary_sentences = []
        word_count = 0
        
        for sentence in sentences[:5]:  # Look at first 5 sentences max
            sentence = sentence.strip()
            if not sentence:
                continue
                
            sentence_words = len(sentence.split())
            if word_count + sentence_words > 100:
                break
                
            summary_sentences.append(sentence)
            word_count += sentence_words
            
            if len(summary_sentences) >= 3:  # Max 3 sentences
                break
        
        fallback_summary = '. '.join(summary_sentences)
        if not fallback_summary.endswith('.'):
            fallback_summary += '.'
            
        return fallback_summary if fallback_summary else content[:200] + "..."
    
    def test_api_connection(self) -> bool:
        """Test if Gemini API is working"""
        try:
            test_response = self.model.generate_content("Test: Respond with 'API Working'")
            return bool(test_response.text)
        except Exception as e:
            self.logger.error(f"API connection test failed: {e}")
            return False
