import streamlit as st
import os
import json
import requests
import urllib.parse

# CONFIG & STYLE (unchanged)
st.set_page_config(page_title="Xbox Tool", page_icon="🎮")
st.markdown(
    '<link rel="apple-touch-icon" href="https://i.imgur.com/27Wxhe3.png" />',
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    body { margin:0; padding:0; }
    .stApp {
        margin-top:0; padding-top:0;
        background-image: url("https://4kwallpapers.com/images/wallpapers/neon-xbox-logo-2880x1800-13434.png");
        background-size: cover; background-position: center; background-repeat: no-repeat; min-height: 100vh;
    }
    header { display:none !important; }
    #MainMenu { visibility:hidden; }
    footer { visibility:hidden; }
    div[data-testid="stHelpSidebar"] { display:none; }
    </style>
    """,
    unsafe_allow_html=True
)

# Header Image
st.markdown(
    '<div style="text-align:center;">'
    '<img src="https://i.imgur.com/uAQOm2Y.png" style="width:600px; max-width:90%; height:auto; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">'
    '</div>',
    unsafe_allow_html=True
)

# Load user data and tokens
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)

if os.path.exists("user_tokens.json"):
    with open("user_tokens.json", "r") as f:
        user_tokens = json.load(f)
else:
    user_tokens = {}  # {username: access_token}

def save_tokens():
    with open("user_tokens.json", "w") as f:
        json.dump(user_tokens, f)

# Helper alert
def show_alert(text):
    st.markdown(f'<div style="background-color:#FFA500; padding:10px; border-radius:5px;">{text}</div>', unsafe_allow_html=True)

# ---- Authentication setup ----
# Replace these with your actual Azure app credentials
CLIENT_ID = "YOUR_CLIENT_ID"  # <-- Replace with your Azure app's Client ID
CLIENT_SECRET = "YOUR_CLIENT_SECRET"  # <-- Replace with your Azure app's Client Secret
REDIRECT_URI = "http://localhost:8501"

def get_oauth_url():
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': 'XboxLive.signin offline_access',
        'response_mode': 'query'
    }
    return f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?{urllib.parse.urlencode(params)}"

# Check if user is logged in
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None

# Login process
if st.session_state['current_user'] is None:
    st.title("Login with Xbox")
    oauth_url = get_oauth_url()
    st.markdown(f"[Click here to login with Microsoft Xbox account]({oauth_url})")
    code_input = st.text_input("Paste the 'code' parameter from URL after login")
    if st.button("Authenticate"):
        if code_input:
            # Exchange code for token
            data = {
                'client_id': CLIENT_ID,
                'scope': 'XboxLive.signin offline_access',
                'code': code_input,
                'redirect_uri': REDIRECT_URI,
                'grant_type': 'authorization_code',
                'client_secret': CLIENT_SECRET
            }
            resp = requests.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data)
            if resp.status_code == 200:
                token = resp.json()['access_token']
                # Ask user for a username to link this account
                username = st.text_input("Enter a username to link this account")
                if st.button("Link Account") and username:
                    users[username] = token
                    save_users()
                    st.session_state['current_user'] = username
                    st.success(f"Account linked as {username}")
            else:
                show_alert("Failed to exchange code for token.")
        else:
            show_alert("Paste the code from URL.")
    st.stop()

# If logged in, show main menu
current_user = st.session_state['current_user']
if current_user and current_user in users:
    token = users[current_user]
    st.title(f"🎮 Xbox Tool - {current_user}")
    st.write("You are logged in with your Xbox account.")
else:
    st.write("Please login to continue.")
    st.stop()

# Main actions
action = st.radio("Select an action:", [
    "Convert Gamertag to XUID",
    "Ban XUID",
    "Spam Messages",
    "Report Spammer",
    "Logout"
])

# Placeholder API call example (replace with real API requests)
def make_api_call(endpoint, params=None):
    headers = {'X-Authorization': token}
    # Example request
    # response = requests.get(f"https://your.api/{endpoint}", headers=headers, params=params)
    # return response.json()
    return {"result": "success", "data": "Fake data"}

# Actions implementations
def convert_gamertag():
    gamertag = st.text_input("Enter Gamertag")
    if st.button("Convert"):
        # Make actual API call here with token
        result = make_api_call("convert_gamertag", {'gamertag': gamertag})
        # Use real response
        st.success(f"Simulated XUID for {gamertag}: 1234567890")

def ban_xuid():
    xuid = st.text_input("Enter XUID to ban")
    if st.button("Confirm Ban"):
        # API call to ban XUID
        make_api_call("ban", {'xuid': xuid})
        st.success(f"XUID {xuid} banned.")

def spam_messages():
    gamertag = st.text_input("Gamertag to spam")
    message = st.text_area("Message")
    count = st.number_input("Number of messages", min_value=1)
    if st.button("Start Spam"):
        for _ in range(int(count)):
            pass
        st.success("Spam sent!")

def report_spammer():
    gamertag = st.text_input("Gamertag to report")
    report_message = st.text_area("Report message")
    count = st.number_input("Number of reports", min_value=1)
    if st.button("Send Reports"):
        for _ in range(int(count)):
            pass
        st.success("Reports sent!")

def logout():
    st.session_state['current_user'] = None
    st.experimental_rerun()

# Dispatch actions
if action == "Convert Gamertag to XUID":
    convert_gamertag()
elif action == "Ban XUID":
    ban_xuid()
elif action == "Spam Messages":
    spam_messages()
elif action == "Report Spammer":
    report_spammer()
elif action == "Logout":
    logout()
