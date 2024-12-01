import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow

def get_credentials():
    credentials = {
        "installed": {
            "client_id": st.secrets.credentials_json.client_id,
            "project_id": st.secrets.credentials_json.project_id,
            "auth_uri": st.secrets.credentials_json.auth_uri,
            "token_uri": st.secrets.credentials_json.token_uri,
            "auth_provider_x509_cert_url": st.secrets.credentials_json.auth_provider_x509_cert_url,
            "client_secret": st.secrets.credentials_json.client_secret,
            "redirect_uris": st.secrets.credentials_json.redirect_uris,
        }
    }
    return credentials

def authenticate_user(SCOPES):
    credentials = get_credentials()
    flow = InstalledAppFlow.from_client_config(credentials, SCOPES)
    creds = flow.run_local_server(port=0)
    return creds

def main():
    print(f"Found the following credentials: {get_credentials()}")

if __name__ == "__main__":
    main()