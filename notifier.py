import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def send_email_notification(subject: str, html_content: str, recipients: list = None) -> bool:
    """
    Sends an email notification via SMTP to one or multiple recipients.
    """
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    sender_email = os.getenv("SENDER_EMAIL") or os.getenv("ALERT_SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD") or os.getenv("GMAIL_APP_PASSWORD")

    # Determine recipients list
    if not recipients:
        recipients = []
        if os.getenv("RECIPIENT_EMAIL"):
            recipients.append(os.getenv("RECIPIENT_EMAIL"))
        if os.getenv("ALERT_RECEIVER_EMAIL") and os.getenv("ALERT_RECEIVER_EMAIL") not in recipients:
            recipients.append(os.getenv("ALERT_RECEIVER_EMAIL"))
        if os.getenv("ALERT_SECONDARY_EMAIL") and os.getenv("ALERT_SECONDARY_EMAIL") not in recipients:
            recipients.append(os.getenv("ALERT_SECONDARY_EMAIL"))
        
        # Fallback if none defined
        if not recipients and sender_email:
            recipients = [sender_email]

    if not sender_email or not sender_password:
        print("[!] Error: SENDER_EMAIL or SENDER_PASSWORD not set in environment (.env).")
        return False

    try:
        # Create message container
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = ", ".join(recipients)

        # Attach HTML body
        part = MIMEText(html_content, "html")
        msg.attach(part)

        # Connect to SMTP server and send
        print(f"[*] Connecting to {smtp_server}:{smtp_port}...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            # sendmail takes a list of recipient strings
            server.sendmail(sender_email, recipients, msg.as_string())
            
        print(f"[+] Email notification successfully sent to: {', '.join(recipients)}")
        return True

    except Exception as e:
        print(f"[!] Failed to send email notification: {e}")
        return False