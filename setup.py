"""
Setup script for AI News Agent
Helps users configure the application interactively
"""

import os
import sys
from pathlib import Path
import yaml

def setup_environment_file():
    """Create .env file from .env.example if it doesn't exist"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if not env_file.exists() and env_example.exists():
        print("Creating .env file from template...")
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print(".env file created! Please edit it with your actual API keys and credentials.")
        return True
    elif env_file.exists():
        print(".env file already exists.")
        return True
    else:
        print(".env.example file not found!")
        return False

def check_config_file():
    """Check if config.yaml exists and is valid"""
    config_file = Path("config/config.yaml")
    
    if not config_file.exists():
        print("config/config.yaml not found!")
        return False
    
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        print("config.yaml found and valid.")
        
        # Check for recipients
        recipients = config.get('email', {}).get('recipients', [])
        if not recipients or recipients[0]['email'] == 'user@example.com':
            print("Please update email recipients in config/config.yaml")
        
        return True
    except Exception as e:
        print(f" Error reading config.yaml: {e}")
        return False

def prompt_for_api_key():
    """Prompt user for Gemini API key"""
    print("\n Gemini API Key Setup")
    print("Get your API key from: https://makersuite.google.com/")
    
    api_key = input("Enter your Gemini API key (or press Enter to skip): ").strip()
    
    if api_key:
        # Update .env file
        env_file = Path(".env")
        if env_file.exists():
            with open(env_file, 'r') as f:
                content = f.read()
            
         
            content = content.replace('GOOGLE_API_KEY_HERE', api_key)
            
            with open(env_file, 'w') as f:
                f.write(content)
            
            print("API key saved to .env file!")
        else:
            print(".env file not found!")

def prompt_for_email():
    """Prompt user for email configuration"""
    print("\nEmail Configuration")
    print("For Gmail, you'll need an App Password (not your regular password)")
    print("Instructions: https://support.google.com/accounts/answer/185833")
    
    email = input("Enter your email address (or press Enter to skip): ").strip()
    
    if email:
        password = input("Enter your email app password (or press Enter to skip): ").strip()
        
        if password:
            env_file = Path(".env")
            if env_file.exists():
                with open(env_file, 'r') as f:
                    content = f.read()
                
                content = content.replace('reelreworks14@gmail.com', email)
                content = content.replace('tvqj igri ocib szvq', password)

                with open(env_file, 'w') as f:
                    f.write(content)
                
                print("Email credentials saved to .env file!")
            else:
                print(".env file not found!")

def update_config_recipients():
    """Update email recipients in config.yaml"""
    print("\nEmail Recipients Configuration")
    
    recipient_email = input("Enter recipient email address (or press Enter to skip): ").strip()
    
    if recipient_email:
        recipient_name = input("Enter recipient name (optional): ").strip() or "AI Enthusiast"
        
        config_file = Path("config/config.yaml")
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            
            # Update recipients
            config['email']['recipients'] = [
                {
                    'email': recipient_email,
                    'name': recipient_name
                }
            ]
            
            with open(config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, indent=2)
            
            print("Recipient updated in config.yaml!")
        else:
            print("config/config.yaml not found!")

def test_setup():
    """Test the setup by running a quick validation"""
    print("\nTesting Configuration...")
    
    try:
        # Add src to path
        sys.path.append(str(Path(__file__).parent / "src"))
        
        from config_manager import ConfigManager
        from logger_config import setup_logging
        
        # Test config loading
        config = ConfigManager()
        logger = setup_logging(config)
        
        print("Configuration loaded successfully!")
        
        # Test Gemini API key
        gemini_key = config.get('gemini.api_key')
        if gemini_key and gemini_key != 'your_gemini_api_key_here':
            print("Gemini API key configured!")
        else:
            print("Gemini API key not configured")
        
        # Test email config
        email_config = config.get_email_config()
        credentials = email_config.get('credentials', {})
        if credentials.get('username') and credentials.get('password'):
            print("Email credentials configured!")
        else:
            print("Email credentials not configured")
        
        return True
        
    except Exception as e:
        print(f"Configuration test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("AI News Agent Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("Please run this script from the AI Agent directory!")
        sys.exit(1)
    
    print("Setting up your AI News Agent...\n")
    
    # Step 1: Create .env file
    if not setup_environment_file():
        print("Setup failed at environment file creation.")
        return
    
    # Step 2: Check config file
    if not check_config_file():
        print("Setup failed at config file validation.")
        return
    
    # Step 3: Interactive configuration
    prompt_for_api_key()
    prompt_for_email()
    update_config_recipients()
    
    # Step 4: Test configuration
    if test_setup():
        print("\nSetup completed successfully!")
        print("\nNext steps:")
        print("1. Run 'python main.py' to test the agent")
        print("2. Check logs/ai_news_agent.log for detailed output")
        print("3. Set up scheduling for daily execution")
    else:
        print("\nSetup completed with warnings.")
        print("Please check your configuration and try running 'python main.py'")

if __name__ == "__main__":
    main()
