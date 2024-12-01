from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText
from manage_credentials import authenticate_user

def create_message(sender, recipient, subject, message_text):
    """
    Creates an email message to be sent via Gmail API.

    Args:
        sender (str): Sender's email address.
        recipient (str): Recipient's email address.
        subject (str): Email subject.
        message_text (str): Body of the email.

    Returns:
        dict: Encoded email message ready for Gmail API.
    """
    message = MIMEText(message_text)
    message["to"] = recipient
    message["from"] = sender
    message["subject"] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {"raw": raw_message}

def send_email(creds, sender, recipient, subject, message_text):
    """
    Sends an email using the Gmail API.

    Args:
        creds (google.oauth2.credentials.Credentials): Authorized credentials object.
        sender (str): Sender's email address.
        to (str): Recipient's email address.
        subject (str): Email subject.
        message_text (str): Body of the email.

    Returns:
        dict: Gmail API response.
    """
    try:
        service = build("gmail", "v1", credentials=creds)
        message = create_message(sender, recipient, subject, message_text)
        sent_message = service.users().messages().send(userId="me", body=message).execute()
        print(f"Email sent to {recipient}: {sent_message['id']}")
        return sent_message
    except Exception as error:
        print(f"An error occurred while sending the email: {error}")
        return None

def main():
    """
    Main function to send an email. Update the sender, recipient, subject, and message_text as needed.
    """
    sender = "karl.frjo@gmail.com"  # Replace with your email
    recipient = "online.ai.production@gmail.com"  # Replace with recipient's email
    subject = "Test Email"
    message_text = "This is a cool showcase!"

    SEND_SCOPE = ["https://www.googleapis.com/auth/gmail.send"]
    creds = authenticate_user(SEND_SCOPE)
    send_email(creds, sender, recipient, subject, message_text)

if __name__ == "__main__":
    main()
