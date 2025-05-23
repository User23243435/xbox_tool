import streamlit as st
import os
import json
import threading
import requests
import asyncio
import aiohttp
import urllib.parse
import itertools

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
    st.stop()

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

# --- Your API keys ---
API_KEYS = [
    "f6835875-3a0b-4fb4-8536-57f785a7912f",
    "0cd3c892-64d1-4275-b39d-6509f39fa557",
    "32f6a5b5-ca4c-41d0-8e60-4c7ba0a1ea69",
    "45598255-0242-4b37-9baa-905f5199a21e",
    "2898954c-5e19-46db-bec3-6b481f267fa8",
    "d45c42ea-113b-44b2-b9ff-33404c4f8b10",
    "8dd211c2-d984-451d-bbd1-920f8d01ba5f",
    "778e5372-5018-44ea-9448-567dd4505e57",
    "15d89583-5fe9-45dd-8dd3-e90f6332bdcf",
    "a95d22bb-6bf5-4bc4-ab39-8526f9c1b7e0",
]
api_key_cycle = itertools.cycle(API_KEYS)

def get_next_api_key():
    return next(api_key_cycle)

# --- Login/Register ---
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

st.title(f"Welcome {st.session_state['current_user']}!")

action = st.radio("Select an action:", [
    "Convert Gamertag to XUID",
    "Ban XUID",
    "Spam Messages",
    "Report Spammer",
    "Logout"
])

# --- Async functions ---
async def convert_gamertag_to_xuid(gamertag):
    url = f"https://xbl.io/api/v2/search/{urllib.parse.quote(gamertag)}"
    headers = {
        "accept": "*/*",
        "x-authorization": get_next_api_key(),
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url, headers=headers)
        data = await resp.json()
        if resp.status != 200:
            print(f"Error fetching XUID: {data}")
            return None
        if "people" in data and len(data["people"]) > 0:
            return data["people"][0]["xuid"]
        return None

async def send_message(xuid, message, session):
    api_key = get_next_api_key()
    url = "https://xbl.io/api/v2/conversations"
    headers = {
        "accept": "*/*",
        "x-authorization": api_key,
        "Content-Type": "application/json"
    }
    payload = {"message": message, "xuid": xuid}
    try:
        resp = await session.post(url, json=payload, headers=headers)
        status = resp.status
        text = await resp.text()
        print(f"Using API key: {api_key}")
        print(f"Response status: {status}")
        print(f"Response body: {text}")

        if status == 200:
            try:
                await resp.json()
                return True
            except Exception as e:
                print(f"JSON decode error: {e}")
                return False
        elif status == 429:
            print("Rate limit hit")
            return "rate_limit"
        else:
            print(f"Error: Status {status}")
            return False
    except Exception as e:
        print(f"Request exception: {e}")
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

# --- UI actions with wait indicator ---
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
        # Implement ban logic here
        st.success(f"XUID {xuid} has been banned.")
elif action == "Spam Messages":
    target_gamertag = st.text_input("Target Gamertag")
    message = st.text_area("Message")
    count = st.number_input("Number of messages", min_value=1)

    # Use session state to track if spam is running
    is_running = st.session_state.get('is_running', False)

    def start_spam():
        st.session_state['is_running'] = True
        st.write("Please wait, sending messages...")

        def run_spam_thread():
            result = asyncio.run(spam_messages(target_gamertag, message, count))
            # After finishing, update state and show message
            st.session_state['is_running'] = False
            if result == "gamertag_not_found":
                st.success("Gamertag not found.")
            elif result == "rate_limit":
                st.warning("Rate limited! Please wait.")
            elif result == "failed":
                st.error("Failed to send some messages.")
            elif result == "done":
                st.success("Finished sending messages.")
            # Rerun to update UI
            st.experimental_rerun()

        threading.Thread(target=run_spam_thread).start()

    start_button = st.button(
        "Start Spam",
        disabled=is_running
    )

    if start_button:
        start_spam()
elif action == "Report Spammer":
    target_gamertag = st.text_input("Gamertag to report")
    reason = st.text_area("Reason")
    count = st.number_input("Number of reports", min_value=1)

    def flood():
        headers = {
            "X-Authorization": get_next_api_key(),
            "Content-Type": "application/json"
        }
        for _ in range(int(count)):
            try:
                requests.post("https://xbl.io/api/report", headers=headers,
                              json={"targetGamertag": target_gamertag, "reason": reason})
            except:
                pass
        st.success(f"Flooded {target_gamertag} with {int(count)} reports.")

    if st.button("Send Reports"):
        threading.Thread(target=flood).start()
        st.success(f"Flooding reports sent to {target_gamertag}.")
        
# --- Logout ---
if action == "Logout":
    st.session_state['current_user'] = None
    safe_rerun()
