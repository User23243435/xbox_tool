import streamlit as st
import asyncio
import aiohttp
import json
import os
import re
import time
import itertools
import urllib.parse

# Helper rerun function
def rerun():
    try:
        st.experimental_rerun()
    except AttributeError:
        st.rerun()

# Initialize users.json with owner if not exists
if not os.path.exists("users.json"):
    users = {
        "SlumpdOWN": {
            "password": "Slumpd9669$",
            "gamertag": "see slumpd",
            "xuid": ""
        }
    }
    with open("users.json", "w") as f:
        json.dump(users, f)
else:
    with open("users.json", "r") as f:
        users = json.load(f)

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)

# Style & Banner
st.set_page_config(page_title="Xbox Tools", page_icon="🎮")
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
    """, unsafe_allow_html=True
)

st.markdown(
    '''
    <div style="text-align:center;">
        <img src="https://i.imgur.com/uAQOm2Y.png" 
             style="width:600px; max-width:90%; height:auto; box-shadow: 0 4px 15px rgba(0,0,0,0.3); margin-top:20px;">
    </div>
    ''', unsafe_allow_html=True
)

# API Keys for convert gamertag to XUID
API_KEYS = [
    "0cd3c892-64d1-4275-b39d-6509f39fa557",
    "32f6a5b5-ca4c-41d0-8e60-4c7ba0a1ea69",
    "45598255-0242-4b37-9baa-905f5199a21e",
    "2898954c-5e19-46db-bec3-6b481f267fa8",
    "d45c42ea-113b-44b2-b9ff-33404c4f8b10",
    "8dd211c2-d984-451d-bbd1-920f8d01ba5f",
    "778e5372-5018-44ea-9448-567dd4505e57",
    "15d89583-5fe9-45dd-8dd3-e90f6332bdcf",
    "a95d22bb-6bf5-4bc4-ab39-8526f9c1b7e0"
]
api_keys_cycle = itertools.cycle(API_KEYS)

async def convert_gamertag_to_xuid(gamertag):
    gamertag = str(gamertag)
    headers = {
        "accept": "*/*",
        "x-authorization": next(api_keys_cycle),
        "Content-Type": "application/json"
    }
    url = f"https://xbl.io/api/v2/search/{urllib.parse.quote(gamertag)}"
    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(url, headers=headers)
            if resp.status != 200:
                return None
            data = await resp.json()
            if "people" in data and len(data["people"]) > 0:
                dec_xuid_str = data["people"][0]["xuid"]
                dec_xuid_int = int(dec_xuid_str)
                hex_xuid = f"{dec_xuid_int:016X}"
                return hex_xuid
            return None
    except:
        return None

# ------------------ UI & Logic ------------------
if 'current_view' not in st.session_state:
    st.session_state['current_view'] = 'login'

# LOGIN / REGISTER SCREEN
if st.session_state['current_view'] == 'login':
    st.title("Register / Login")
    mode = st.radio("Mode", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Register flow
    if mode == "Register":
        st.write("**Example URL:** https://www.xbox.com/en-US/play/user/User1234")
        profile_link = st.text_input("Paste your Xbox profile link (full URL)")

        if st.button("Verify Profile Link"):
            # Validate URL input
            if not profile_link:
                st.error("Please paste your Xbox profile URL.")
            else:
                match = re.search(r"/user/([^/]+)", profile_link)
                if not match:
                    st.error("Invalid URL format. Please ensure it's the correct Xbox profile URL.")
                else:
                    gamertag = urllib.parse.unquote(match.group(1))
                    with st.spinner("Verifying gamertag..."):
                        xuid = asyncio.run(convert_gamertag_to_xuid(gamertag))
                    if xuid:
                        st.success(f"Verified! Gamertag: {gamertag} (XUID: {xuid})")
                        st.session_state['verified_gamertag'] = gamertag
                        st.session_state['verified_xuid'] = xuid
                    else:
                        st.error("Gamertag not found or verification failed.")

        # Registration button validation
        if st.button("Register"):
            if not username:
                st.error("Please enter a username to register.")
            elif not password:
                st.error("Please enter a password.")
            elif 'verified_gamertag' not in st.session_state:
                st.error("You must verify your profile link before registering.")
            elif username in users:
                st.error("Username already exists. Please choose a different username.")
            else:
                # Save new user
                users[username] = {
                    'password': password,
                    'gamertag': st.session_state['verified_gamertag'],
                    'xuid': st.session_state['verified_xuid']
                }
                save_users()
                st.success("Registration successful! Please login.")
                st.experimental_rerun()

    # Login flow
    elif st.button("Login"):
        if not username:
            st.error("Please enter your username.")
        elif not password:
            st.error("Please enter your password.")
        else:
            if username in users and users[username]['password'] == password:
                st.session_state['current_user'] = username
                st.session_state['profile'] = users[username]
                st.session_state['current_view'] = 'main'
                st.experimental_rerun()
            else:
                st.error("Invalid username or password.")

# MAIN DASHBOARD
elif st.session_state['current_view'] == 'main':
    user = st.session_state['profile']
    username = st.session_state['current_user']

    # Show owner info if owner logs in
    if username == "SlumpdOWN":
        st.markdown("### 👑 **Admin**")
        profile_url = "https://www.xbox.com/en-US/play/user/see%20slumpd"
        st.write(f"Profile URL: {profile_url}")
        xuid = user.get('xuid') or asyncio.run(convert_gamertag_to_xuid(user.get('gamertag')))
        st.write(f"XUID: {xuid}")
    else:
        st.markdown("### User")
        st.write(f"Logged in as: {username}")

    linked_gt = user.get('gamertag')
    linked_xuid = user.get('xuid')

    if linked_gt:
        st.write(f"**Linked Gamertag:** {linked_gt}")
        if st.button("Unlink Gamertag"):
            users[username].pop('gamertag', None)
            users[username].pop('xuid', None)
            save_users()
            st.success("Gamertag unlinked.")
            st.experimental_rerun()

        st.write(f"**XUID:** {linked_xuid if linked_xuid else 'N/A'}")
    else:
        st.write("No gamertag linked.")
        st.write("### Link a new Gamertag")
        profile_url = st.text_input("Paste Xbox profile URL")
        if st.button("Verify and Link") and profile_url:
            if not profile_url:
                st.error("Please paste your Xbox profile URL.")
            else:
                match = re.search(r"/user/([^/]+)", profile_url)
                if not match:
                    st.error("Invalid URL. Please ensure the URL is correct.")
                else:
                    gamertag = urllib.parse.unquote(match.group(1))
                    with st.spinner("Verifying gamertag..."):
                        xuid = asyncio.run(convert_gamertag_to_xuid(gamertag))
                    if xuid:
                        # Check if gamertag already linked elsewhere
                        already_linked = False
                        for u, d in users.items():
                            if d.get('gamertag') == gamertag and u != username:
                                already_linked = True
                                break
                        if already_linked:
                            st.error("This gamertag is linked to another user.")
                        elif gamertag == linked_gt:
                            st.info("Already linked.")
                        else:
                            users[username]['gamertag'] = gamertag
                            users[username]['xuid'] = xuid
                            save_users()
                            st.success("Gamertag linked successfully.")
                            st.experimental_rerun()
                    else:
                        st.error("Gamertag not found.")

    # --------- Tools menu placeholder ---------
    st.write("## Tools")
    if st.button("Open Tools Menu"):
        st.session_state['show_tools'] = True

    if st.session_state.get('show_tools'):
        with st.sidebar:
            st.markdown("### Tools Menu")
            choice = st.selectbox("Choose Tool", [
                "Convert Gamertag to XUID",
                "Spam Banner Message",
                "Flood Reports",
                "Ban XUID"
            ])

            if choice == "Convert Gamertag to XUID":
                gt_input = st.text_input("Gamertag")
                if st.button("Convert to XUID"):
                    with st.spinner("Converting..."):
                        result = asyncio.run(convert_gamertag_to_xuid(gt_input))
                    if result:
                        st.success(f"XUID: {result}")
                    else:
                        st.error("Gamertag not found.")
            elif choice == "Spam Banner Message":
                msg = st.text_area("Message to spam")
                count = st.number_input("Number of messages", min_value=1, max_value=1000, value=10)
                if st.button("Start Spamming"):
                    def spam():
                        for _ in range(count):
                            # Placeholder for actual banner message
                            print(f"[Banner]: {msg}")
                            time.sleep(0.5)
                    threading.Thread(target=spam).start()
                    st.success("Started spamming.")
            elif choice == "Flood Reports":
                target_gt = st.text_input("Target Gamertag")
                report_msg = st.text_area("Report message")
                count = st.number_input("Number of reports", min_value=1, max_value=100, value=30)
                if st.button("Flood Reports"):
                    def flood():
                        for _ in range(count):
                            # Placeholder for report
                            print(f"[Report]: {target_gt} - {report_msg}")
                            time.sleep(0.2)
                    threading.Thread(target=flood).start()
                    st.success("Flooding reports...")
            elif choice == "Ban XUID":
                xuid_ban = st.text_input("XUID to ban")
                if st.button("Ban"):
                    banned = set()
                    if os.path.exists("banned_xuids.json"):
                        with open("banned_xuids.json", "r") as f:
                            banned = set(json.load(f))
                    banned.add(xuid_ban)
                    with open("banned_xuids.json", "w") as f:
                        json.dump(list(banned), f)
                    st.success("XUID banned.")

    # --------- Logout ---------
    if st.button("Logout"):
        st.session_state.clear()
        rerun()
