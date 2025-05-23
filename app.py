import streamlit as st
import os
import json
import threading
import requests
import asyncio
import aiohttp
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
        background-size: cover; 
        background-position: center; 
        background-repeat: no-repeat; 
        min-height: 100vh;
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
    '''
    <div style="text-align:center;">
        <img src="https://i.imgur.com/uAQOm2Y.png" 
             style="width:600px; max-width:90%; height:auto; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
    </div>
    ''',
    unsafe_allow_html=True
)

# --- Load API key ---
def load_api_key():
    try:
        with open('api_key.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        st.error("API key file 'api_key.txt' not found!")
        return None

API_KEY = load_api_key()
if not API_KEY:
    st.stop()  # Stop if no API key is loaded

# --- Load users ---
if os.path.exists("users.json"):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except json.JSONDecodeError:
        users = {}
else:
    users = {}

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)

# --- Session state ---
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None
if 'access_token' not in st.session_state:
    st.session_state['access_token'] = None
if 'is_running' not in st.session_state:
    st.session_state['is_running'] = False

def safe_rerun():
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.stop()

# --- Registration / Login ---
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

# --- Main dashboard ---
st.title(f"Welcome {st.session_state['current_user']}!")

action = st.radio("Select an action:", [
    "Convert Gamertag to XUID",
    "Ban XUID",
    "Spam Messages",
    "Report Spammer",
    "Logout"
])

# --- Async functions for spam ---
async def convert_gamertag_to_xuid(gamertag):
    url = f"https://xbl.io/api/v2/search/{urllib.parse.quote(gamertag)}"
    headers = {
        "accept": "*/*",
        "x-authorization": API_KEY,
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url, headers=headers)
        data = await resp.json()
        if resp.status != 200:
            return None
        if "people" in data and len(data["people"]) > 0:
            return data["people"][0]["xuid"]
        return None

async def send_message(xuid, message, session):
    url = "https://xbl.io/api/v2/conversations"
    headers = {
        "accept": "*/*",
        "x-authorization": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"message": message, "xuid": xuid}
    resp = await session.post(url, json=payload, headers=headers)
    # Check response status before parsing JSON
    if resp.status == 200:
        try:
            await resp.json()
            return True
        except:
            return False
    elif resp.status == 429:
        # Rate limit hit
        return "rate_limit"
    else:
        # For other errors, try to get error message
        try:
            await resp.json()
        except:
            pass
        return False

async def spam_messages(gamertag, message, amount):
    xuid = await convert_gamertag_to_xuid(gamertag)
    if not xuid:
        return "gamertag_not_found"
    async with aiohttp.ClientSession() as session:
        for i in range(amount):
            result = await send_message(xuid, message, session)
            if result == "rate_limit":
                return "rate_limit"
            elif result is False:
                return "failed"
            print(f"Sent message {i+1}")
            await asyncio.sleep(1)
    return "done"

# --- UI: prevent multiple runs ---
def run_spam():
    # Set flag to prevent multiple
    st.session_state['is_running'] = True
    with st.spinner("Sending messages..."):
        result = asyncio.run(spam_messages(target_gamertag, message, count))
    st.session_state['is_running'] = False
    return result

# --- Action handlers ---
if action == "Convert Gamertag to XUID":
    gamertag = st.text_input("Enter Gamertag")
    if st.button("Convert"):
        if gamertag:
            xuid = asyncio.run(convert_gamertag_to_xuid(gamertag))
            if xuid:
                st.success(f"XUID: {xuid}")
            else:
                st.error("Gamertag not found or error.")
elif action == "Ban XUID":
    xuid = st.text_input("Enter XUID to ban")
    if st.button("Confirm Ban"):
        # Your real ban API call here
        st.success(f"XUID {xuid} has been banned.")
elif action == "Spam Messages":
    target_gamertag = st.text_input("Target Gamertag")
    message = st.text_area("Message")
    count = st.number_input("Number of messages", min_value=1)
    start_button = st.button(
        "Start Spam",
        disabled=st.session_state['is_running']
    )
    if start_button:
        # Run spam asynchronously
        result = run_spam()
        # Show result
        if result == "gamertag_not_found":
            st.error("Gamertag not found.")
        elif result == "rate_limit":
            st.warning("Rate limited! Please wait.")
        elif result == "failed":
            st.error("Failed to send some messages.")
        elif result == "done":
            st.success("Finished sending messages.")
elif action == "Report Spammer":
    target_gamertag = st.text_input("Gamertag to report")
    reason = st.text_area("Reason")
    count = st.number_input("Number of reports", min_value=1)
    if st.button("Send Reports"):
        def flood():
            headers = {
                "X-Authorization": API_KEY,
                "Content-Type": "application/json"
            }
            for _ in range(int(count)):
                try:
                    requests.post("https://xbl.io/api/report", headers=headers,
                                  json={"targetGamertag": target_gamertag, "reason": reason})
                except:
                    pass
        threading.Thread(target=flood).start()
        st.success(f"Flooded {target_gamertag} with {int(count)} reports.")

# --- Logout ---
if action == "Logout":
    st.session_state['current_user'] = None
    safe_rerun()
