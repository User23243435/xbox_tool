import streamlit as st
import os
import asyncio
import json
import random

# 1. Configure the page
st.set_page_config(page_title="Xbox Tool", page_icon="🎮")

# 2. Custom icon
st.markdown(
    '<link rel="apple-touch-icon" href="https://i.imgur.com/27Wxhe3.png" />',
    unsafe_allow_html=True
)

# 3. Style background & hide default menu/footer
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

# 4. Header image
st.markdown(
    '<div style="text-align:center;">'
    '<img src="https://i.imgur.com/uAQOm2Y.png" style="width:600px; max-width:90%; height:auto; box-shadow:0 4px 15px rgba(0,0,0,0.3);">'
    '</div>',
    unsafe_allow_html=True
)

# --- Your alert box helper ---
def show_alert(text):
    st.markdown(f'<div style="background-color:#FFA500; padding:10px; border-radius:5px;">{text}</div>', unsafe_allow_html=True)

# Load/save users
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)

# Load/save access tokens for OAuth
if os.path.exists("access_tokens.json"):
    with open("access_tokens.json", "r") as f:
        access_tokens = json.load(f)
else:
    access_tokens = {}

def save_access_tokens():
    with open("access_tokens.json", "w") as f:
        json.dump(access_tokens, f)

# Your API key load
def load_api_key():
    try:
        with open('api_key.txt', 'r') as f:
            return f.read().strip()
    except:
        st.error("Missing api_key.txt! Please create this file with your API key.")
        st.stop()

API_KEY = load_api_key()
REPORT_API_URL = "https://xbl.io/api/report"  # <-- replace with actual endpoint

# -------------- OAuth login functions --------------
def get_oauth_url():
    params = {
        'client_id': 'YOUR_CLIENT_ID',  # replace
        'response_type': 'code',
        'redirect_uri': 'http://localhost:8501/auth/callback',
        'scope': 'XboxLive.signin offline_access',
        'response_mode': 'query'
    }
    return f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?{urllib.parse.urlencode(params)}"

async def exchange_code_for_token_async(code):
    data = {
        'client_id': 'YOUR_CLIENT_ID',        # replace
        'scope': 'XboxLive.signin offline_access',
        'code': code,
        'redirect_uri': 'http://localhost:8501/auth/callback',
        'grant_type': 'authorization_code',
        'client_secret': 'YOUR_CLIENT_SECRET'   # replace
    }
    resp = requests.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data)
    if resp.status_code == 200:
        return resp.json()['access_token']
    else:
        return None

# -------------- Check if logged in with OAuth --------------
if 'oauth_logged_in' not in st.session_state:
    st.session_state['oauth_logged_in'] = False
if 'oauth_token' not in st.session_state:
    st.session_state['oauth_token'] = ''

# -------------- Main app logic --------------
if not st.session_state['oauth_logged_in']:
    # Show only OAuth login option
    st.title("Login with Microsoft to continue")
    st.markdown(f"[Click here to login with Microsoft]({get_oauth_url()})")
    st.write("After login, paste the 'code' parameter from the URL below.")
    code_input = st.text_input("Paste 'code' from URL after login:")
    if st.button("Login with Microsoft"):
        if code_input:
            token = asyncio.run(exchange_code_for_token_async(code_input))
            if token:
                st.session_state['oauth_logged_in'] = True
                st.session_state['oauth_token'] = token
                st.success("Successfully logged in with Microsoft!")
            else:
                show_alert("Failed to authenticate. Please try again.")
        else:
            show_alert("Please paste the 'code' from URL.")
    st.stop()  # prevent anything else until logged in

# Now, the user is logged in with OAuth, show main menu
st.title("Xbox Tool")
st.write("You are logged in with Microsoft OAuth. Use the menu below.")


# Main menu
action = st.radio("Select an action:", [
    "Convert Gamertag to XUID",
    "Ban XUID",
    "Spam Messages",
    "Report Spammer",
    "Logout"
])

# -------------- Actions --------------
if action == "Convert Gamertag to XUID":
    gamertag = st.text_input("Enter Gamertag")
    if st.button("Convert"):
        # simulate async call
        xuid = asyncio.run(asyncio.sleep(1, result="1234567890"))
        st.success(f"XUID: {xuid}")

elif action == "Ban XUID":
    xuid = st.text_input("Enter XUID to ban")
    if st.button("Confirm Ban"):
        st.success(f"XUID {xuid} banned!")

elif action == "Spam Messages":
    gamertag = st.text_input("Gamertag to spam")
    message = st.text_area("Message")
    count = st.number_input("Number of messages", min_value=1)
    if st.button("Start Spam"):
        for _ in range(int(count)):
            pass
        st.success("Spam sent!")

elif action == "Report Spammer":
    gamertag = st.text_input("Gamertag to report")
    report_message = st.text_area("Report message")
    count = st.number_input("Number of reports", min_value=1)
    if st.button("Send Reports"):
        for _ in range(int(count)):
            pass
        st.success("Reports sent!")

elif action == "Logout":
    st.session_state['oauth_logged_in'] = False
    st.session_state['oauth_token'] = ''
    st.experimental_rerun()
