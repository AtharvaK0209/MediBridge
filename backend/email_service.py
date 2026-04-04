import smtplib
import os
from email.mime.text import MIMEText

def send_expiry_alert(email, expired_count, near_count):
    try:
        sender_email = os.environ.get("MAIL_SENDER", "atharvaak8056@gmail.com")
        app_password = os.environ.get("MAIL_APP_PASSWORD", "kbpr pzgi gqbp cxen")

        subject = "Medicine Expiry Alert"

        body = f"""
Hello,

This is an automated alert from MediBridge.

Expired medicines: {expired_count}
Near expiry medicines: {near_count}

Please review your pharmacy inventory.

Regards,
Team MediBridge
"""

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()

    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send alert to {email}: {e}")