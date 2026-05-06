import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from hope.configuration import settings as config

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    """Gets the Gmail API service instance."""
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists(config.GMAIL_TOKEN):
        creds = Credentials.from_authorized_user_file(config.GMAIL_TOKEN, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(config.GMAIL_CREDS):
                raise FileNotFoundError(f"Credentials file not found at {config.GMAIL_CREDS}. Please follow setup instructions.")
            
            flow = InstalledAppFlow.from_client_secrets_file(config.GMAIL_CREDS, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(config.GMAIL_TOKEN, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def read_unread_emails():
    """Returns a list of unread email summaries."""
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId='me', q='is:unread', maxResults=5).execute()
        messages = results.get('messages', [])

        if not messages:
            return []

        summaries = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            payload = msg['payload']
            headers = payload.get('headers')
            
            subject = "No Subject"
            sender = "Unknown Sender"
            
            for header in headers:
                if header.get('name') == 'Subject':
                    subject = header.get('value')
                if header.get('name') == 'From':
                    sender = header.get('value')
            
            summaries.append({"sender": sender, "subject": subject})
            
        return summaries
    except Exception as e:
        print(f"Gmail API Error (Read): {e}")
        return None

def send_email(to, subject, body):
    """Sends an email using the Gmail API."""
    try:
        service = get_gmail_service()
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        send_msg = {'raw': raw_message}
        
        service.users().messages().send(userId='me', body=send_msg).execute()
        return True
    except Exception as e:
        print(f"Gmail API Error (Send): {e}")
        return False
