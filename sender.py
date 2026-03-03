"""
sender.py — Sends the rendered digest via Gmail SMTP.
Uses Gmail App Password (not your regular Gmail password).

Setup:
  1. Enable 2FA on your Google account
  2. Go to: myaccount.google.com/apppasswords
  3. Create an app password → use that as GMAIL_APP_PASSWORD secret
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timezone
from config import SENDER_EMAIL, RECIPIENT_EMAIL, GMAIL_APP_PASSWORD


def send_digest(html_body: str, plain_body: str):
    today = datetime.now(timezone.utc).strftime("%B %d, %Y")
    subject = f"🤖 AI/ML Digest — {today}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"AI Digest <{SENDER_EMAIL}>"
    msg["To"]      = RECIPIENT_EMAIL

    # Attach plain text first, HTML second (email clients prefer last)
    msg.attach(MIMEText(plain_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    print("[Sender] Connecting to Gmail SMTP...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())

    print(f"[Sender] ✅ Email sent to {RECIPIENT_EMAIL}")
