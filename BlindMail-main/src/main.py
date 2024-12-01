import streamlit as st
from extract_mails import fetch_emails
from manage_credentials import authenticate_user
from ai_prediction import Prediction
from ai_voice_to_text import get_user_input
from ai_text_to_voice import text_to_voice

# Setup Google API scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

def load_css(file_path):
    """Load CSS from an external file."""
    with open(file_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'conversation_active' not in st.session_state:
        st.session_state.conversation_active = False
    if 'creds' not in st.session_state:
        st.session_state.creds = None
    if 'emails' not in st.session_state:
        st.session_state.emails = []
    if 'hf_token' not in st.session_state:
        st.session_state.hf_token = ""

def toggle_conversation():
    """Toggle the conversation state and authenticate if needed."""
    st.session_state.conversation_active = not st.session_state.conversation_active
    if st.session_state.conversation_active and not st.session_state.creds:
        st.session_state.creds = authenticate_user(SCOPES)
        st.session_state.emails = fetch_emails(st.session_state.creds)
        print(st.session_state.hf_token)
        st.session_state.hf_token = st.secrets["hf_token"]
        print(st.session_state.hf_token)

def render_ui():
    """Render the main UI components of the Streamlit app."""
    # Set up the page
    st.set_page_config(
        page_title="Blind Mail",
        page_icon="👀",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    # Load external CSS
    load_css("src/styles.css")

    # Add Title and Subtitle
    st.title("👀 Blind Mail 👀")
    st.subheader("🗣️ Gemma2-powered Voice Emails 🗣️")
    st.markdown("""---""")

def handle_start_conversation():
    emails = st.session_state.emails
    print(f"Emails: {emails}")
    if not emails:
        text_to_voice("You don't have any unread emails.")
        pass
    else:
        text_to_voice(f"You have {len(emails)} unread emails. Would you like to summarize or reply to them?")
        pass
    print("finished start convo")

def handle_email_actions(prediction):
    """Handle user actions with fetched emails."""
    # Get email information
    user_input = get_user_input()
    print(user_input)
    print("Starting first prediction")
    prediction.obtain_actions(user_input) # returns reply or summarize
    print("Starting first prediction")
    # to-do: preprocessing to get just one email specified by user
    
    # to-do: select correct email
    selection_index = prediction.create_reply(user_input, st.session_state.emails)
    print(f"Selected email index: {selection_index}")
    
    result = prediction.main(user_input, st.session_state.emails, selection_index) # returns emails response OR email summary
    print(f"AI Response: {result}")
    
    # text_to_voice(result)
    # senders = [email['sender'] for email in emails]
    # subjects = [email['subject'] for email in emails]
    # bodies = [email['body'] for email in emails]
    
    # LOGIC FOR GEMMA2 - USER INTERACTION
    
    
    # user_input = wait for user until voice-to-text callback
    
    
    # To-Do: 
    # 
    
    
        
def main():
    """Main application logic."""
    # Initialize session state
    initialize_session_state()

    # Render the UI
    render_ui()

    # Start/stop conversation button
    button_label = "Start Conversation" if not st.session_state.conversation_active else "Stop Conversation"
    if st.button(button_label, key="toggle_button", on_click=toggle_conversation):
        pass
    
    

    # Handle active conversation
    if st.session_state.conversation_active:
        print("CONVERSATION ACTIVE")
        if st.session_state.creds:
            st.success("🟢 Conversation is active.")
            prediction = Prediction(st.session_state.hf_token)
            print("CREDENTIALS SET")
            handle_start_conversation()
            # while st.session_state.conversation_active:
            handle_email_actions(prediction)
            st.markdown("""---""")
    else:
        st.warning("🔴 Conversation is stopped.")

if __name__ == "__main__":
    main()