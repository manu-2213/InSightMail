# **BlindMail**
## **Empowering Communication for the Visually Impaired**

BlindMail is thoughtfully crafted to enhance accessibility, enabling individuals who are blind to seamlessly manage and communicate through their Gmail inbox. Leveraging the advanced Gemma 2 model, BlindMail transforms email interaction into an intuitive and natural language experience.

## **Key Features:**
- Email Summarization: Quickly grasp the essence of your messages with concise and clear summaries.
- Smart Email Responses: Effortlessly reply to emails using intelligent, context-aware suggestions.
- AI-Powered Email Drafting: Compose well-articulated emails with the assistance of our sophisticated AI drafting tool.
- Experience a more accessible and efficient way to stay connected with BlindMail—where technology meets inclusivity.

## **Local & Online Re-Deployment using Streamlit**
### **Step 1: Create a Google Cloud Project**

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. In the top left corner, click on the **Select a Project** dropdown and click **New Project**.
3. Provide a name for your project and click **Create**.

### **Step 2: Enable APIs**

1. After creating your project, go to the [APIs & Services Dashboard](https://console.cloud.google.com/apis/dashboard).
2. Search for the [Gmail API](https://console.cloud.google.com/apis/library/gmail.googleapis.com?) and enable it.

### **Step 3: Create OAuth 2.0 Credentials**

1. Go to the **Credentials** page in the Google Cloud Console: [Credentials Page](https://console.cloud.google.com/apis/credentials).
2. Click **Create Credentials** and select **OAuth 2.0 Client IDs**.
3. In the **Create OAuth client ID** page:
   - For **Application type**, choose **Web application**.
   - Set **Authorized JavaScript origins** to `http://localhost` (for local development).
   - Set **Authorized redirect URIs** to `http://localhost`.
4. Click **Create**. You will now see your **Client ID** and **Client Secret**.

### **Step 4: Download Credentials**

1. After creating the OAuth client ID, click the **Download** button next to your new credentials. This will download a `credentials.json` file.
2. **Important:** Store this file securely and do not share it publicly.

### **Step 5 - Local Deployment: Create a local secrets.toml file**
To authenticate your Streamlit application with Google Cloud services, you need to provide your credentials securely. Follow these steps to create a `secrets.toml` file:

1. Create the `secrets.toml` File inside the `.streamlit` directory

    - Linux:

            touch .streamlit/secrets.toml    

    - Windows:

            nano .streamlit/secrets.toml
    
2. Copy-paste the following content and replace the placeholders with your actual credentials:

        [credentials_json.installed]
        client_id = "your_client_id"
        project_id = "your_project_id"
        auth_uri = "https://accounts.google.com/o/oauth2/auth"
        token_uri = "https://oauth2.googleapis.com/token"
        auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
        client_secret = "your_client_secret"
        redirect_uris = ["http://localhost"]


3. Run the application (Locally)

        streamlit run src/main.py


### **Step 5 - Online Deployment: Copy-paste the credentials into Streamlit Share**

1. Create a new project and upload your code using one of the provided methods.

2. Copy-paste your local "secrets.toml" file's content into "Advanced Settings" -> "Secrets" and click "Deploy".

For further details please take a look at the official [Streamlit Secrets Management documentation](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management).

## **Authors: Queen Mary University of London - Machine Learning Society (QMML)**