import streamlit as st
import asyncio
import json
import os
import random

# --------- Set favicon to controller emoji ---------
st.markdown(
    """
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 height=%22124%22 width=%22124%22><text y=%22.9em%22 font-size=%22.10000000000000001em%22>🎮</text></svg>">
    """,
    unsafe_allow_html=True
)

# --------- Constants ---------
BACKGROUND_URL = "https://4kwallpapers.com/images/wallpapers/neon-xbox-logo-2880x1800-13434.png"
HEADER_IMAGE_URL = "https://i.imgur.com/uAQOm2Y.png"

# --------- Function definitions ---------

def generate_captcha():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    return f"What is {a} + {b}?", a + b

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)

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

async def convert_gamertag_to_xuid(gamertag):
    await asyncio.sleep(1)
    return "1234567890"

async def send_message(xuid, message, number):
    await asyncio.sleep(0.5)
    return True

async def spam_messages(gamertag, message, count):
    xuid = await convert_gamertag_to_xuid(gamertag)
    for i in range(count):
        await send_message(xuid, message, i+1)

async def report_spammer(gamertag, message, count):
    xuid = await convert_gamertag_to_xuid(gamertag)
    for i in range(count):
        await send_message(xuid, message, i+1)

# --------- Main app ---------
def main():
    # Load or initialize users
    global users
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            users = json.load(f)
    else:
        users = {}

    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'user' not in st.session_state:
        st.session_state['user'] = ''

    # Inject font style for better readability
    if 'font_injected' not in st.session_state:
        st.markdown(
            """
            <style>
            body {
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                font-size: 18px;
                line-height: 1.6;
                color: white; /* ensure text contrast */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.session_state['font_injected'] = True

    # Inject background CSS only once
    if 'bg_injected' not in st.session_state:
        st.markdown(
            f"""
            <style>
            /* Full-page background image */
            .stApp {{
                background-image: url("{BACKGROUND_URL}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                min-height: 100vh;
            }}
            </style>
            """, unsafe_allow_html=True
        )
        st.session_state['bg_injected'] = True

    # App content container
    with st.container():
        # Big header image (no border, styled)
        st.markdown(
            f'<div style="text-align:center;">'
            f'<img src="{HEADER_IMAGE_URL}" style="width:600px; max-width:90%; height:auto; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">'
            f'</div>',
            unsafe_allow_html=True
        )

        # Hide default Streamlit UI
        st.markdown(
            """
            <style>
            header {display: none !important;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            div[data-testid="stHelpSidebar"] {display: none;}
            </style>
            """, unsafe_allow_html=True
        )

        # Authentication
        if not st.session_state['logged_in']:
            choice = st.radio("Create account or login:", ["Login", "Register"])
            if choice == "Login":
                login()
            else:
                register()
            if not st.session_state['logged_in']:
                return

        # Main menu options
        st.title("Xbox Tool - Main Menu")
        option = st.radio("Choose an action:", [
            "Convert Gamertag to XUID",
            "Ban XUID",
            "Spam Messages",
            "Report Spammer",
            "Logout"
        ])

        if option == "Convert Gamertag to XUID":
            gamertag = st.text_input("Enter Gamertag")
            if st.button("Convert"):
                xuid = asyncio.run(convert_gamertag_to_xuid(gamertag))
                st.success(f"XUID: {xuid}")

        elif option == "Ban XUID":
            xuid = st.text_input("Enter XUID to ban")
            if st.button("Confirm Ban"):
                st.success(f"XUID {xuid} banned!")

        elif option == "Spam Messages":
            gamertag = st.text_input("Gamertag to spam")
            message = st.text_area("Message")
            count = st.number_input("Number of messages", min_value=1)
            if st.button("Start Spam"):
                asyncio.run(spam_messages(gamertag, message, int(count)))
                st.success("Spam sent!")

        elif option == "Report Spammer":
            gamertag = st.text_input("Gamertag to report")
            report_message = st.text_area("Report message")
            count = st.number_input("Number of reports", min_value=1)
            if st.button("Send Reports"):
                asyncio.run(report_spammer(gamertag, report_message, int(count)))
                st.success("Reports sent!")

        elif option == "Logout":
            st.session_state['logged_in'] = False
            st.session_state['user'] = ""
            st.experimental_rerun()

if __name__ == "__main__":
    main()
