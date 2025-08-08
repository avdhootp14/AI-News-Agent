"""Email sending functionality for AI News Agent"""

import smtplib
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict
from dotenv import load_dotenv

load_dotenv()


class EmailSender:
    """Sends formatted emails using SMTP"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger('ai_news_agent.email_sender')

        # Get email configuration
        email_config = self.config.get_email_config()
        smtp_config = email_config.get('smtp', {})

        self.smtp_server = smtp_config.get('server', 'smtp.gmail.com')
        self.smtp_port = smtp_config.get('port', 587)
        self.use_tls = smtp_config.get('use_tls', True)

        # Credentials come ONLY from .env
        self.username = os.getenv("EMAIL_USERNAME")
        self.password = os.getenv("EMAIL_PASSWORD")

        if not self.username or not self.password:
            raise ValueError("SMTP_USER or SMTP_PASSWORD not set in .env")

        # Recipients from YAML
        self.recipients = email_config.get('recipients', [])
        if not self.recipients:
            raise ValueError("No email recipients configured")

    def send_email(self, email_content: Dict[str, str]) -> bool:
        """
        Send email with the provided content

        Args:
            email_content: Dictionary with 'subject', 'html_body', 'text_body'

        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            self.logger.info("Preparing to send email")

            # Create the base message
            msg = self._create_message(email_content)

            # Send email
            self._send_via_smtp(msg)

            self.logger.info(f"Email sent successfully to {len(self.recipients)} recipients")
            return True

        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            return False

    def _create_message(self, email_content: Dict[str, str]) -> MIMEMultipart:
        """Create MIME message from email content"""

        msg = MIMEMultipart('alternative')
        msg['Subject'] = email_content['subject']
        msg['From'] = self.username
        msg['To'] = ', '.join([recipient['email'] for recipient in self.recipients])

        # Add text and HTML parts
        text_part = MIMEText(email_content['text_body'], 'plain', 'utf-8')
        html_part = MIMEText(email_content['html_body'], 'html', 'utf-8')

        msg.attach(text_part)
        msg.attach(html_part)

        return msg

    def _send_via_smtp(self, msg: MIMEMultipart):
        """Send message via SMTP"""

        self.logger.debug(f"Connecting to SMTP server: {self.smtp_server}:{self.smtp_port}")

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            if self.use_tls:
                server.starttls()
                self.logger.debug("TLS enabled")

            server.login(self.username, self.password)
            self.logger.debug("SMTP login successful")

            # Send individually to each recipient
            recipient_emails = [recipient['email'] for recipient in self.recipients]

            for recipient_email in recipient_emails:
                try:
                    individual_msg = MIMEMultipart('alternative')
                    individual_msg['Subject'] = msg['Subject']
                    individual_msg['From'] = msg['From']
                    individual_msg['To'] = recipient_email

                    # Attach parts
                    for part in msg.walk():
                        if part.get_content_type() in ['text/plain', 'text/html']:
                            individual_msg.attach(part)

                    server.send_message(individual_msg)
                    self.logger.debug(f"Email sent to: {recipient_email}")

                except Exception as e:
                    self.logger.error(f"Failed to send to {recipient_email}: {e}")
                    continue

    def test_email_connection(self) -> bool:
        """Test email connection and credentials"""
        try:
            self.logger.info("Testing email connection")

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)

            self.logger.info("Email connection test successful")
            return True

        except Exception as e:
            self.logger.error(f"Email connection test failed: {e}")
            return False

    def send_test_email(self) -> bool:
        """Send a test email to verify everything is working"""
        try:
            test_content = {
                'subject': 'AI News Agent - Test Email',
                'html_body': '''
                <html>
                <body>
                    <h2>AI News Agent Test</h2>
                    <p>This is a test email to verify that your AI News Agent is configured correctly.</p>
                    <p>If you're receiving this, everything is working properly!</p>
                    <p><strong>AI News Agent</strong></p>
                </body>
                </html>
                ''',
                'text_body': '''
AI News Agent Test

This is a test email to verify that your AI News Agent is configured correctly.

If you're receiving this, everything is working properly!

AI News Agent
                '''
            }

            return self.send_email(test_content)

        except Exception as e:
            self.logger.error(f"Failed to send test email: {e}")
            return False
