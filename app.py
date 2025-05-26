import streamlit as st
import asyncio
import aiohttp
import json
import os
import re
import time
import itertools
import threading
import urllib.parse

# --- Helper function for rerunning app ---
def rerun():
    try:
        st.experimental_rerun()
    except AttributeError:
        # Fallback for older versions
        try:
            st.rerun()
        except:
            pass  # Cannot rerun, user must refresh

# --- Save users data ---
def save_users():
    with open(users_file, "w") as f:
        json.dump(users, f)

# --- Initialize users data ---
users_file = "users.json"
if not os.path.exists(users_file):
    users = {
        "SlumpdOWN": {
            "password": "Slumpd9669$",
            "gamertag": "see slumpd",
            "xuid": ""
        }
    }
    with open(users_file, "w") as f:
        json.dump(users, f)
else:
    try:
        with open(users_file, "r") as f:
            users = json.load(f)
        if not isinstance(users, dict):
            raise json.JSONDecodeError("Invalid format", "", 0)
    except:
        users = {
            "SlumpdOWN": {
                "password": "Slumpd9669$",
                "gamertag": "see slumpd",
                "xuid": ""
            }
        }
        with open(users_file, "w") as f:
            json.dump(users, f)

# --- Style & background + neon + glow for small text ---
st.set_page_config(page_title="Xbox Tools", page_icon="🎮")
st.markdown(
    """
    <style>
    body { margin:0; padding:0; }
    .stApp {
        margin-top:0; padding-top:0;
        background-image: url("https://i.imgur.com/wg6k91A.jpeg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        min-height: 100vh;
    }
    header { display:none !important; }
    #MainMenu { visibility:hidden; }
    footer { visibility:hidden; }
    div[data-testid="stHelpSidebar"] { display:none; }
    /* Neon style for headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Orbitron', sans-serif;
        color: #00ffff;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
    }
    /* Neon style for buttons */
    button {
        background-color: #00ffff;
        border: none;
        padding: 12px 24px;
        border-radius: 50px;
        font-weight: 700;
        cursor: pointer;
        font-family: 'Orbitron', sans-serif;
        transition: all 0.3s ease;
        color: #000;
    }
    button:hover {
        background-color: #00cccc;
        transform: scale(1.05);
    }
    /* Input fields */
    input[type=text], input[type=password], textarea, select, input[type=number] {
        width: 100%;
        padding: 14px 20px;
        margin-top: 8px;
        margin-bottom: 15px;
        border-radius: 10px;
        border: none;
        background: rgba(255,255,255,0.2);
        color: #00ffff;
        font-family: 'Orbitron', sans-serif;
        font-size: 1em;
    }
    input[type=text]:focus, input[type=password]:focus, textarea:focus {
        background: rgba(255,255,255,0.3);
        box-shadow: 0 0 10px #00ffff;
    }
    /* Small text glow instructions */
    .small-text {
        color: #00ffff;
        font-family: 'Orbitron', sans-serif;
        font-size: 1em;
        text-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff;
    }
    </style>
    """, unsafe_allow_html=True
)

# --- Banner Logo ---
st.markdown("""
<div style="text-align:center;">
    <img src="https://i.imgur.com/uAQOm2Y.png" 
         style="width:600px; max-width:90%; height:auto; box-shadow: 0 4px 15px rgba(0,0,0,0.3); margin-top:20px;">
</div>
""", unsafe_allow_html=True)

# --- API Keys ---
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

# --- Function to convert gamertag to XUID ---
async def convert_gamertag_to_xuid(gamertag):
    api_keys = API_KEYS
    cycle = itertools.cycle(api_keys)
    headers = {
        "accept": "*/*",
        "x-authorization": next(cycle),
        "Content-Type": "application/json"
    }
    gamertag_str = str(gamertag) if gamertag else ""
    url = f"https://xbl.io/api/v2/search/{urllib.parse.quote(gamertag_str)}"
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

# --- Main app logic ---
if 'current_view' not in st.session_state:
    st.session_state['current_view'] = 'login'
if 'profile' not in st.session_state:
    st.session_state['profile'] = None

# --- Login/Register Screen ---
if st.session_state['current_view'] == 'login':
    with st.container():
        st.title("🎮 Welcome to Xbox Tools")
        mode = st.radio("Mode", ["Login", "Register"], index=0)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if mode == "Register":
            # Small instruction
            st.markdown('<div class="small-text">**Example Profile URL:**</div>', unsafe_allow_html=True)
            st.write("https://www.xbox.com/en-US/play/user/User1234")
            profile_link = st.text_input("Paste your Xbox profile link (full URL)")

            if st.button("Verify Profile Link"):
                if not profile_link:
                    st.error("Please paste your profile URL.")
                else:
                    match = re.search(r"/user/([^/]+)", profile_link)
                    if not match:
                        st.error("Invalid URL format.")
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

            if st.button("Register"):
                if not username:
                    st.error("Please enter a username")
                elif not password:
                    st.error("Please enter a password")
                elif 'verified_gamertag' not in st.session_state:
                    st.error("Verify your profile link first")
                elif username in users:
                    st.error("Username already exists")
                else:
                    users[username] = {
                        "password": password,
                        "gamertag": st.session_state['verified_gamertag'],
                        "xuid": st.session_state['verified_xuid']
                    }
                    save_users()
                    st.success("Registration complete! Please login.")
                    st.experimental_rerun()

        elif st.button("Login"):
            if not username:
                st.error("Enter username")
            elif not password:
                st.error("Enter password")
            elif username in users and users[username]['password'] == password:
                st.session_state['current_user'] = username
                st.session_state['profile'] = users[username]
                st.session_state['current_view'] = 'main'
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")


# --- Main Dashboard ---
elif st.session_state['current_view'] == 'main':
    user = st.session_state['profile']
    username = st.session_state['current_user']

    # Admin info
    if username == "SlumpdOWN":
        st.markdown("### 👑 Admin Dashboard")
        st.write("Profile URL: https://www.xbox.com/en-US/play/user/see%20slumpd")
        xuid = user.get('xuid') or asyncio.run(convert_gamertag_to_xuid(user.get('gamertag')))
        st.write(f"XUID: {xuid}")
    else:
        st.markdown("### User Dashboard")
        st.write(f"Logged in as: {username}")

    linked_gt = user.get('gamertag')
    linked_xuid = user.get('xuid')

    if linked_gt:
        st.markdown(f"**Linked Gamertag:** {linked_gt}")
        if st.button("Unlink Gamertag"):
            users[username].pop('gamertag', None)
            users[username].pop('xuid', None)
            save_users()
            st.success("Gamertag unlinked.")
            st.experimental_rerun()
        st.markdown(f"**XUID:** {linked_xuid if linked_xuid else 'N/A'}")
    else:
        # Small instruction
        st.markdown('<div class="small-text">**Link a new Gamertag:**</div>', unsafe_allow_html=True)
        profile_url = st.text_input("Paste Xbox profile URL")
        if st.button("Verify & Link") and profile_url:
            match = re.search(r"/user/([^/]+)", profile_url)
            if not match:
                st.error("Invalid URL")
            else:
                gamertag = urllib.parse.unquote(match.group(1))
                with st.spinner("Verifying..."):
                    xuid = asyncio.run(convert_gamertag_to_xuid(gamertag))
                if xuid:
                    # Check if already linked
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

    # --- Sidebar for tools ---
    st.sidebar.title("Tools")
    selected_tool = st.sidebar.selectbox("Select Tool", [
        "Convert Gamertag to XUID",
        "Spam Banner Message",
        "Flood Reports",
        "Ban XUID"
    ])

    # --- Tool: Convert Gamertag to XUID ---
    if selected_tool == "Convert Gamertag to XUID":
        st.title("Convert Gamertag to XUID")
        gamertag_input = st.text_input("Enter Gamertag")
        if st.button("Convert"):
            with st.spinner("Converting..."):
                result = asyncio.run(convert_gamertag_to_xuid(gamertag_input))
            if result:
                st.success(f"XUID: {result}")
            else:
                st.error("Gamertag not found or error.")

    # --- Tool: Spam Banner Message ---
    elif selected_tool == "Spam Banner Message":
        st.title("Spam Banner Message")
        target_gt = st.text_input("Target Gamertag (who to spam)")
        message = st.text_area("Message to spam")
        count = st.slider("Number of messages", 1, 50, 10)
        if st.button("Start Spamming"):
            def spam():
                for i in range(count):
                    # Simulate "sending" message
                    st.write(f"🔥 Sending to {target_gt}: {message} ({i+1}/{count})")
                    time.sleep(0.5)
            threading.Thread(target=spam).start()
            st.success(f"Started spamming {count} messages to {target_gt}!")

    # --- Tool: Flood Reports ---
    elif selected_tool == "Flood Reports":
        st.title("Flood Reports")
        target_gt = st.text_input("Target Gamertag")
        report_message = st.text_area("Report message")
        count = st.slider("Number of reports", 1, 100, 30)
        if st.button("Flood Reports"):
            def flood():
                for i in range(count):
                    st.write(f"🚩 Reporting: {target_gt} - {report_message} ({i+1}/{count})")
                    time.sleep(0.2)
            threading.Thread(target=flood).start()
            st.success("Flooding reports...")

    # --- Tool: Ban XUID ---
    elif selected_tool == "Ban XUID":
        st.title("Ban XUID")
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

    # --- Logout button ---
    if st.button("Logout"):
        st.session_state.clear()
        rerun()
