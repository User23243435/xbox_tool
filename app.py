import streamlit as st
import json
import os
import asyncio
import random
import aiohttp

# --- Hide Streamlit default menu, header, footer, and top icons ---
st.set_page_config(page_title="Xbox Tool", layout="centered")
st.markdown(
    """
    <style>
    header {display: none !important;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stHelpSidebar"] {display: none;}
    @media (max-width: 768px) {
        img.header-img {
            width: 70% !important;
        }
        h1, h2, h3, h4, h5, h6 {
            font-size: calc(1.2em + 1vw) !important;
        }
        .block-container {
            flex-direction: column !important;
        }
        button, input[type=text], input[type=password], textarea, input[type=number] {
            width: 100% !important;
            font-size: 1.2em;
            padding: 12px;
        }
        .css-1d391kg {
            padding: 10px !important;
        }
        img {
            max-width: 80% !important;
            height: auto !important;
        }
    }
    </style>
    """, unsafe_allow_html=True
)

# --- Embed header image ---
header_image_url = "https://i.imgur.com/WhRBcgw.png"

# --- Background ---
background_url = "https://4kwallpapers.com/images/wallpapers/xbox-logo-black-background-amoled-gradient-5k-1920x1200-3285.png"
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        min-height: 100vh;
        width: 100%;
        position: relative;
        color: #fff;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background-color: rgba(0,0,0,0.3);
        z-index: -1;
    }}
    img.header-img {{
        width: 50%;
        max-width: 350px;
        height: auto;
        display: block;
        margin: 10px auto;
    }}
    </style>
    """, unsafe_allow_html=True
)

# --- Show header ---
st.markdown(
    f'<img src="{header_image_url}" class="header-img" alt="XBOX TOOL">',
    unsafe_allow_html=True
)

# --- Load or initialize users ---
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

# --- Session state ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = ''

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)

def generate_captcha():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    return f"What is {a} + {b}?", a + b

# --- API key for gamertag to XUID ---
API_KEY = "YOUR_API_KEY_HERE"  # <-- Replace with your actual API key

# --- Convert gamertag to XUID function ---
async def convert_gamertag_to_xuid(gamertag):
    url = f"https://xbl.io/api/v2/search/{gamertag}"
    headers = {
        "accept": "*/*",
        "x-authorization": API_KEY,
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url, headers=headers)
        if resp.status != 200:
            return None
        data = await resp.json()
        if "people" in data and len(data["people"]) > 0 and "xuid" in data["people"][0]:
            return data["people"][0]["xuid"]
        return None

# --- Register ---
def register():
    st.subheader("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    confirm = st.text_input("Confirm Password", type='password')
    if 'captcha_q' not in st.session_state:
        q, a = generate_captcha()
        st.session_state['captcha_q'] = q
        st.session_state['captcha_a'] = a
    captcha_input = st.text_input(st.session_state['captcha_q'])
    if st.button("Register"):
        if username in users:
            st.error("🛑 Username exists")
        elif password != confirm:
            st.error("🛑 Passwords don't match")
        elif captcha_input != str(st.session_state['captcha_a']):
            st.error("🛑 Wrong captcha")
        elif not password:
            st.error("🛑 Password cannot be empty")
        else:
            users[username] = password
            save_users()
            st.success("✅ Registered! Please login.")
            q, a = generate_captcha()
            st.session_state['captcha_q'], st.session_state['captcha_a'] = q, a

# --- Login ---
def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if 'captcha_q' not in st.session_state:
        q, a = generate_captcha()
        st.session_state['captcha_q'] = q
        st.session_state['captcha_a'] = a
    captcha_input = st.text_input(st.session_state['captcha_q'])
    if st.button("Login"):
        if captcha_input != str(st.session_state['captcha_a']):
            st.error("🛑 Wrong captcha")
        elif username in users and users[username] == password:
            st.session_state['logged_in'] = True
            st.session_state['user'] = username
            st.success(f"✅ Welcome {username}!")
            q, a = generate_captcha()
            st.session_state['captcha_q'], st.session_state['captcha_a'] = q, a
        else:
            st.error("🛑 Wrong username or password")
            q, a = generate_captcha()
            st.session_state['captcha_q'], st.session_state['captcha_a'] = q, a

# --- Main app ---
def main():
    if not st.session_state['logged_in']:
        choice = st.radio("Create account or login:", ["Login", "Register"])
        if choice == "Login":
            login()
        else:
            register()
        return

    # Main interface
    st.write(f"Logged in as: {st.session_state['user']}")

    # --- Gamertag to XUID ---
    st.subheader("Gamertag to XUID Conversion")
    gamertag_input = st.text_input("Enter Gamertag")
    if st.button("Convert to XUID"):
        if gamertag_input:
            # Call async function
            xuid = asyncio.run(convert_gamertag_to_xuid(gamertag_input))
            if xuid:
                st.success(f"XUID: {xuid}")
            else:
                st.error("Failed to get XUID. Check API key or gamertag.")

    # --- Ban XUID ---
    st.subheader("Ban XUID")
    xuid_to_ban = st.text_input("Enter XUID to ban")
    if st.button("Ban XUID"):
        # Placeholder for banning logic
        st.success(f"XUID {xuid_to_ban} banned!")

    # --- Spam Messages ---
    st.subheader("Spam Messages")
    spam_gamertag = st.text_input("Gamertag to spam")
    spam_message = st.text_area("Message")
    spam_count = st.number_input("Number of messages", min_value=1, value=1)
    if st.button("Start Spamming"):
        if spam_gamertag and spam_message:
            asyncio.run(spam_messages(spam_gamertag, spam_message, int(spam_count)))
            st.success("Spam sent!")

    # --- Report Spammer ---
    st.subheader("Report Spammer")
    report_gamertag = st.text_input("Gamertag to report")
    report_message = st.text_area("Report message")
    report_count = st.number_input("Number of reports", min_value=1, value=1)
    if st.button("Send Reports"):
        if report_gamertag and report_message:
            asyncio.run(report_spammer(report_gamertag, report_message, int(report_count)))
            st.success("Reports sent!")

    # --- Logout ---
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['user'] = ""
        st.experimental_rerun()

# --- Async functions for spam and report ---
async def spam_messages(gamertag, message, count):
    xuid = await convert_gamertag_to_xuid(gamertag)
    if not xuid:
        return
    for _ in range(count):
        await asyncio.sleep(0.1)  # simulate delay
        # Here you'd implement actual message sending logic
        # For now, just print to console
        print(f"Sent message to XUID {xuid}: {message}")

async def report_spammer(gamertag, message, count):
    xuid = await convert_gamertag_to_xuid(gamertag)
    if not xuid:
        return
    for _ in range(count):
        await asyncio.sleep(0.1)
        # Implement actual report logic here
        print(f"Reported XUID {xuid}: {message}")

if __name__ == "__main__":
    main()
