import streamlit as st
import os
import json
import asyncio
import requests
import threading
import urllib.parse

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

# Header Image
st.markdown(
    '<div style="text-align:center;">'
    '<img src="https://i.imgur.com/uAQOm2Y.png" style="width:600px; max-width:90%; height:auto; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">'
    '</div>',
    unsafe_allow_html=True
)

# --- Load users (register/login) ---
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        try:
            users = json.load(f)
            if not isinstance(users, dict):
                users = {}
            else:
                for u, data in list(users.items()):
                    if not isinstance(data, dict) or 'password' not in data:
                        if isinstance(data, str):
                            users[u] = {'password': data}
                        else:
                            users[u] = {}
        except:
            users = {}
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

# --- Session state ---
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None
if 'access_token' not in st.session_state:
    st.session_state['access_token'] = None

# --- Helper for rerun ---
def safe_rerun():
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        # fallback: just stop; user can refresh
        st.stop()

# --- Registration/Login UI ---
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
                st.error("Username already exists.")
            else:
                users[username] = {'password': password}
                save_users()
                st.success("Registration successful! Please login.")
        else:
            if (
                username in users 
                and isinstance(users[username], dict) 
                and users[username].get('password') == password
            ):
                st.session_state['current_user'] = username
                st.success(f"Logged in as {username}")
                safe_rerun()
            else:
                st.error("Invalid username or password")
    st.stop()

# --- Main Dashboard ---
st.title(f"Welcome {st.session_state['current_user']}!")

action = st.radio("Select an action:", [
    "Convert Gamertag to XUID",
    "Ban XUID",
    "Spam Messages",
    "Report Spammer",
    "Logout"
])

# --- Placeholder API functions ---
def make_api_call(endpoint, params=None):
    # Implement your real API call here
    return {"status": "success", "data": "Fake data"}

async def convert_gamertag_to_xuid(gamertag):
    headers = {
        "accept": "*/*",
        "x-authorization": API_KEY,
        "Content-Type": "application/json"
    }
    url = f"https://xbl.io/api/v2/search/{urllib.parse.quote(gamertag)}"
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            return None
        data = resp.json()
        if "people" in data and len(data["people"]) > 0:
            return data["people"][0]["xuid"]
        return None
    except:
        return None

def flood_reports(access_token, target_gamertag, message, count=30):
    def report():
        for _ in range(count):
            try:
                headers = {
                    "X-Authorization": access_token,
                    "Content-Type": "application/json"
                }
                data = {
                    "targetGamertag": target_gamertag,
                    "reason": message
                }
                requests.post("https://xbl.io/api/report", headers=headers, json=data)
            except:
                pass
    threading.Thread(target=report).start()

# --- Action Handlers ---
if action == "Convert Gamertag to XUID":
    gamertag = st.text_input("Enter Gamertag")
    if st.button("Convert"):
        if gamertag:
            xuid = asyncio.run(convert_gamertag_to_xuid(gamertag))
            if xuid:
                st.success(f"XUID: {xuid}")
            else:
                st.error("Gamertag not found or error occurred.")
elif action == "Ban XUID":
    xuid = st.text_input("Enter XUID to ban")
    if st.button("Confirm Ban"):
        # Your real ban API call here
        st.success(f"XUID {xuid} has been banned.")
elif action == "Spam Messages":
    target_gamertag = st.text_input("Target Gamertag")
    message = st.text_area("Message")
    count = st.number_input("Number of messages", min_value=1)
    if st.button("Start Spam"):
        for _ in range(int(count)):
            pass
        st.success(f"Sent {count} spam messages to {target_gamertag}.")
elif action == "Report Spammer":
    target_gamertag = st.text_input("Gamertag to report")
    report_message = st.text_area("Reason")
    count = st.number_input("Number of reports", min_value=1)
    if st.button("Send Reports"):
        flood_reports(st.session_state.get('access_token'), target_gamertag, report_message, int(count))
        st.success(f"Flooded {target_gamertag} with {int(count)} reports.")
elif action == "Logout":
    st.session_state['current_user'] = None
    st.session_state['access_token'] = None
    safe_rerun()
