import streamlit as st
import os
import json
import requests
import threading
import time

# --- Set page config ---
st.set_page_config(page_title="Xbox Tool", page_icon="🎮")

# --- Custom style ---
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

# --- Header image ---
st.markdown(
    '<div style="text-align:center;">'
    '<img src="https://i.imgur.com/uAQOm2Y.png" style="width:600px; max-width:90%; height:auto; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">'
    '</div>',
    unsafe_allow_html=True
)

# --- Load or initialize users ---
users_path = "users.json"
if os.path.exists(users_path):
    try:
        with open(users_path, "r") as f:
            users = json.load(f)
        if not isinstance(users, dict):
            users = {}
    except:
        users = {}
else:
    users = {}

def save_users():
    with open(users_path, "w") as f:
        json.dump(users, f)

# --- Fixed API key ---
API_KEY = "8bdd-8041d82bb8e4"

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
                st.error("Please fill in both username and password.")
            elif username in users:
                st.error("Username already exists.")
            else:
                users[username] = {'password': password}
                save_users()
                st.success("Registration successful! Please login.")
        else:  # Login
            if username in users and users[username]['password'] == password:
                st.session_state['current_user'] = username
                st.success(f"Logged in as {username}")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")
    st.stop()

# --- Main app ---
st.title(f"Welcome {st.session_state['current_user']}!")

action = st.radio("Choose an action:", [
    "Convert Gamertag to XUID",
    "Ban XUID",
    "Spam Messages",
    "Report Spammer",
    "Logout"
])

# Helper functions

def make_api_call(endpoint, params=None):
    # Placeholder for real API calls
    # Replace with actual API logic as needed
    return {"status": "success", "data": "Fake data"}

def convert_gamertag():
    gamertag = st.text_input("Gamertag")
    if st.button("Convert"):
        # Simulate API call
        result = make_api_call("convert_gamertag", {'gamertag': gamertag})
        st.success(f"Simulated XUID for {gamertag}: 1234567890")

def ban_xuid():
    xuid = st.text_input("XUID to ban")
    if st.button("Ban XUID"):
        make_api_call("ban_xuid", {'xuid': xuid})
        st.success(f"Banned XUID {xuid}")

def spam_messages():
    gamertag = st.text_input("Gamertag to spam")
    message = st.text_area("Message")
    count = st.number_input("Number of messages", min_value=1, max_value=100)
    if st.button("Spam"):
        # Simulate spamming
        for _ in range(int(count)):
            pass
        st.success("Spam messages sent!")

def report_spammer():
    gamertag = st.text_input("Gamertag to report")
    report_message = st.text_area("Report message")
    count = st.number_input("Number of reports", min_value=1, max_value=50)
    if st.button("Send reports"):
        # Simulate reporting
        for _ in range(int(count)):
            pass
        st.success("Reports sent!")

def logout():
    st.session_state['current_user'] = None
    st.success("Logged out.")
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
