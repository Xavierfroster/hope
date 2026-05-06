import smtplib
import imaplib
import email
import os
from hope.configuration import settings as config
from hope.communication import gmail_api
from hope.core.engine import speak

def hope_speak(message, raw=False):
    # This will be passed from features.py or we import it
    speak(message)

def send_email(to, content):
    """Sends email via Gmail API (OAuth2) if configured, otherwise falls back to SMTP."""
    if os.path.exists(config.GMAIL_CREDS) or os.path.exists(config.GMAIL_TOKEN):
        success = gmail_api.send_email(to, "Message from HOPE", content)
        if success:
            return True

    # Fallback to legacy SMTP
    try:
        user = config.EMAIL_USER
        password = config.EMAIL_PASS
        if not user or not password or "your" in user:
            return False
            
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(user, password)
        server.sendmail(user, to, content)
        server.close()
        return True
    except Exception:
        return False

def read_emails():
    """Reads unread emails using Gmail API (OAuth2) with fallback to IMAP."""
    # Try OAuth2 first
    if os.path.exists(config.GMAIL_CREDS) or os.path.exists(config.GMAIL_TOKEN):
        try:
            summaries = gmail_api.read_unread_emails()
            if summaries is not None:
                if not summaries:
                    return "Your inbox is as empty as a desert. No new emails."

                report = f"You have {len(summaries)} unread emails. Here are the latest ones.\n"
                for s in summaries:
                    report += f"From {s['sender']}. Subject: {s['subject']}\n"
                return report
        except Exception:
            pass

    # Fallback to legacy IMAP
    try:
        user = config.EMAIL_USER
        password = config.EMAIL_PASS
        
        if not user or not password or "your" in user:
            return "I need OAuth2 credentials or an App Password to read your emails."

        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(user, password)
        mail.select("inbox")
        
        status, data = mail.search(None, 'UNSEEN')
        mail_ids = data[0].split()
        
        if not mail_ids:
            return "Your inbox is as empty as a desert. No new emails."

        report = f"You have {len(mail_ids)} unread emails. Here are the latest ones.\n"
        for i in mail_ids[-3:]:
            status, data = mail.fetch(i, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = msg['subject']
                    sender = msg['from']
                    report += f"From {sender}. Subject: {subject}\n"
        
        mail.logout()
        return report
    except Exception as e:
        return f"Failed to read emails: {e}"
