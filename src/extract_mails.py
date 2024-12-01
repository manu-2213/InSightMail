from googleapiclient.discovery import build
import base64
from manage_credentials import authenticate_user

def decode_base64(data):
    return base64.urlsafe_b64decode(data).decode("utf-8")

def fetch_emails(creds):
    try:
        service = build("gmail", "v1", credentials=creds)
        results = service.users().messages().list(userId="me", maxResults=10).execute()
        messages = results.get("messages", [])

        email_texts = []

        if not messages:
            print("No messages found.")
        else:
            print("Fetching email content...")
            for message in messages:
                msg = service.users().messages().get(userId="me", id=message["id"], format="full").execute()
                payload = msg.get("payload", {})
                parts = payload.get("parts", [])
                for part in parts:
                    if part["mimeType"] == "text/plain":
                        data = part["body"]["data"]
                        text = decode_base64(data)
                        email_texts.append(text)

        return email_texts

    except Exception as error:
        print(f"An error occurred: {error}")
        return []

def main():
    READ_SCOPE = ["https://www.googleapis.com/auth/gmail.readonly"]
    creds = authenticate_user(READ_SCOPE)
    emails = fetch_emails(creds)

    if not emails:
        print("No emails to summarize.")
        return

    print("Original Email Content:")
    for idx, email in enumerate(emails):
        print(f"\nEmail {idx + 1}:\n{email}\n")

if __name__ == "__main__":
    main()
