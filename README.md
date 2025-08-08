# 🤖 AI Daily News Agent

An intelligent automation system that delivers personalized daily news summaries directly to your email inbox. The agent scrapes latest news, uses AI to create concise summaries, and sends them automatically every morning.

## ✨ Features

- **🔄 Automated Daily Delivery**: Runs automatically every morning at 8:00 AM IST
- **🤖 AI-Powered Summaries**: Uses Google Gemini AI to create intelligent news summaries
- **📧 Email Integration**: Sends formatted news directly to your email
- **☁️ Cloud-Based**: Runs on GitHub Actions - no need to keep your computer on
- **🆓 Completely Free**: Utilizes GitHub's free tier for automation
- **⚙️ Configurable**: Easy to customize news sources and email preferences
- **📱 Mobile Friendly**: Receive news summaries on any device

## 🚀 Quick Start

### Prerequisites

- GitHub account
- Gmail account with App Password enabled
- Google Gemini API key

### Setup Instructions

1. **Fork/Clone this repository**
   ```bash
   git clone https://github.com/yourusername/ai-news-agent.git
   cd ai-news-agent
   ```

2. **Get Required API Keys**
   - **Gemini API**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey) to get your free API key
   - **Gmail App Password**: Enable 2FA on Gmail, then generate an app password

## ⚙️ Configuration

### Environment Variables

Create a `.env` file for local development:

```env
GEMINI_API_KEY=your_gemini_api_key
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

### Customization Options

- **Schedule**: Modify the cron expression in `.github/workflows/daily-news-agent.yml`
- **Email Template**: Customize the HTML template in `agents/email_agent.py`
- **News Sources**: Add/modify news sources in `utils/news_scraper.py`
- **AI Prompts**: Adjust summarization prompts in `utils/ai_summarizer.py`

## 🔧 Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Run Locally**
   ```bash
   python main.py
   ```

## 🛠️ Technical Details

### Technologies Used

- **Python 3.11+**: Core programming language
- **Google Gemini AI**: Advanced language model for summarization
- **GitHub Actions**: CI/CD and automation platform
- **SMTP/Gmail**: Email delivery service
- **BeautifulSoup4**: Web scraping library
- **Requests**: HTTP library for API calls

### Key Components

- **News Scraper**: Fetches latest news from multiple sources
- **AI Summarizer**: Creates concise, relevant summaries using Gemini
- **Email Agent**: Formats and sends professional-looking emails
- **Config Manager**: Handles environment variables and settings
- **Automation Workflow**: GitHub Actions for scheduled execution

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ and AI**

*Never miss important news again! Get your daily dose of information delivered fresh to your inbox every morning.*