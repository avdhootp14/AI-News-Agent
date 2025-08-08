import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

smtp_user = os.getenv("EMAIL_USERNAME")
smtp_password = os.getenv("EMAIL_PASSWORD")

recipient_email = "avdhoot144@gmail.com"

msg = MIMEText("This is a test email from SMTP_USER to a different recipient.")
msg["Subject"] = "Test Email"
msg["From"] = smtp_user
msg["To"] = recipient_email

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.send_message(msg)

print("Email sent successfully.")
