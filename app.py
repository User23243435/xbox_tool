import streamlit as st
import os
import json

# --- CONFIG & STYLE ---
st.set_page_config(page_title="Xbox Tool", page_icon="🎮")
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

st.markdown(
    '<div style="text-align:center;">'
    '<img src="https://i.imgur.com/uAQOm2Y.png" style="width:600px; max-width:90%; height:auto; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">'
    '</div>',
    unsafe_allow_html=True
)

# --- Load users ---
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)

# --- Load API key ---
def load_api_key():
    try:
        with open('api_key.txt', 'r') as f:
            return f.read().strip()
    except:
        st.error("Missing api_key.txt! Please create this file with your API key.")
        st.stop()

API_KEY = load_api_key()

# --- Login/Register ---
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None

if not st.session_state['current_user']:
    st.markdown("### Welcome! Please Register or Login")
    mode = st.radio("Mode", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        if mode == "Register":
            if not username or not password:
                st.error("Fill in username and password")
            elif username in users:
                st.error("Username exists")
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
                st.error("Invalid username/password")
    st.stop()

# --- Main Menu ---
st.title(f"Welcome {st.session_state['current_user']}!")

action = st.radio("Select an action:", [
    "Convert Gamertag to XUID",
    "Ban XUID",
    "Spam Messages",
    "Report Spammer",
    "Logout"
])

def make_api_call(endpoint, params=None):
    # Placeholder for real API call
    return {"status": "success", "data": "Fake data"}

def convert_gamertag():
    gamertag = st.text_input("Enter Gamertag")
    if st.button("Convert"):
        # Replace with real API call
        xuid = "1234567890"
        st.success(f"XUID for {gamertag}: {xuid}")

def ban_xuid():
    xuid = st.text_input("Enter XUID to ban")
    if st.button("Confirm Ban"):
        # Replace with real API call
        st.success(f"XUID {xuid} banned!")

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

# --- Execute action ---
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
