import streamlit as st
import os
import json
import requests

# --- 1. Set page config ---
st.set_page_config(page_title="Xbox Tool", page_icon="🎮")

# --- 2. Custom style ---
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

# --- 3. Header image ---
st.markdown(
    '<div style="text-align:center;">'
    '<img src="https://i.imgur.com/uAQOm2Y.png" style="width:600px; max-width:90%; height:auto; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">'
    '</div>',
    unsafe_allow_html=True
)

# --- 4. Load users and save functions ---
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)

# --- 5. Validate API key ---
# Use your fixed API key
API_KEY = "8bdd-8041d82bb8e4"

def validate_api_key(api_key):
    url = "https://xbl.io/api/v5/account/ownership"
    headers = {'X-Auth': api_key}
    try:
        response = requests.get(url, headers=headers)
        return response.status_code == 200
    except:
        return False

# --- 6. Manage login state ---
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None

# --- 7. If not logged in, show login/register ---
if not st.session_state['current_user']:
    st.markdown("### Welcome! Please Register or Login")
    mode = st.radio("Mode", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Submit"):
        if mode == "Register":
            if username in users:
                st.error("Username already exists.")
            else:
                users[username] = {'password': password}
                save_users()
                st.success("Registered! Please login.")
        else:
            if username in users and users[username]['password'] == password:
                st.session_state['current_user'] = username
                st.success(f"Logged in as {username}")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")
    st.stop()

# --- 8. Logged in, show main app ---
st.title(f"Welcome {st.session_state['current_user']}!")

action = st.radio("Choose an action:", [
    "Convert Gamertag to XUID",
    "Ban XUID",
    "Spam Messages",
    "Report Spammer",
    "Logout"
])

def make_api_call(endpoint, params=None):
    headers = {'X-Auth': API_KEY}
    url_map = {
        "convert_gamertag": "https://xbl.io/api/v5/xuid/convert",
        "ban_xuid": "https://xbl.io/api/v5/xuid/ban",
        "spam_messages": "https://xbl.io/api/v5/messages/spam",
        "report_spammer": "https://xbl.io/api/v5/report"
    }
    url = url_map.get(endpoint)
    # Here, you should implement real API call logic.
    # For now, just simulate success.
    return {"status": "success", "data": "Fake data"}

def convert_gamertag():
    gamertag = st.text_input("Gamertag")
    if st.button("Convert"):
        result = make_api_call("convert_gamertag", {'gamertag': gamertag})
        st.success(f"Simulated XUID: 1234567890 for {gamertag}")

def ban_xuid():
    xuid = st.text_input("XUID to ban")
    if st.button("Ban XUID"):
        make_api_call("ban_xuid", {'xuid': xuid})
        st.success(f"Banned XUID {xuid}")

def spam_messages():
    gamertag = st.text_input("Gamertag to spam")
    message = st.text_area("Message")
    count = st.number_input("Number of messages", min_value=1)
    if st.button("Spam"):
        for _ in range(int(count)):
            pass
        st.success("Spam sent!")

def report_spammer():
    gamertag = st.text_input("Gamertag to report")
    report_message = st.text_area("Report message")
    count = st.number_input("Number of reports", min_value=1)
    if st.button("Send reports"):
        for _ in range(int(count)):
            pass
        st.success("Reports sent!")

def logout():
    st.session_state['current_user'] = None
    st.experimental_rerun()

# Run selected action
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
