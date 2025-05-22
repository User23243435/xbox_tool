import streamlit as st
import json
import os
import asyncio
import random

# --- All your functions here ---

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)

def generate_captcha():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    return f"What is {a} + {b}?", a + b

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

def main():
    # Load or initialize users data
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

    # Your background image URL
    background_image_url = "https://4kwallpapers.com/images/wallpapers/neon-xbox-logo-2880x1800-13434.png"
    # Your banner image URL
    banner_image_url = "https://i.imgur.com/u5Lf7fu.png"

    # Inject background CSS
    st.markdown(
        f"""
        <style>
        /* Full-page background container */
        .background-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('{background_image_url}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            z-index: -1;
        }}
        /* Optional overlay for contrast */
        /* .overlay {{
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background-color: rgba(0,0,0,0.3);
            z-index: -1;
        }} */
        /* Main content above background */
        .main-content {{
            position: relative;
            z-index: 1;
            padding: 20px;
        }}
        /* Floating logo style */
        .floating-logo {{
            position: fixed;
            top: 20px;
            right: 20px;
            width: 150px;
            height: 150px;
            z-index: 9999;
            pointer-events: none;
            opacity: 0.8;
            animation: float 3s ease-in-out infinite;
        }}
        @keyframes float {{
            0% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0); }}
        }}
        </style>
        <div class="background-container"></div>
        """,
        unsafe_allow_html=True
    )

    # Wrap app content inside a container
    with st.container():
        # Banner image
        st.markdown(
            f'<img src="{banner_image_url}" style="width:100%; max-width:600px; display:block; margin:auto;">',
            unsafe_allow_html=True
        )

        # Floating Xbox GIF
        xbox_logo_gif = "https://media.giphy.com/media/3oKIPwoe7Xh7e5Yv4w/giphy.gif"
        st.markdown(
            f"""
            <div class="floating-logo">
                <img src="{xbox_logo_gif}" style="width:100%; height:auto;">
            </div>
            """,
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
            """,
            unsafe_allow_html=True
        )

        # Authentication flow
        if not st.session_state.get('logged_in', False):
            choice = st.radio("Create account or login:", ["Login", "Register"])
            if choice == "Login":
                login()
            else:
                register()
            # Exit if not logged in
            if not st.session_state.get('logged_in', False):
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
            st.subheader("Convert Gamertag to XUID")
            gamertag = st.text_input("Enter Gamertag")
            if st.button("Convert"):
                with st.spinner('Converting...'):
                    xuid = asyncio.run(convert_gamertag_to_xuid(gamertag))
                st.success(f"XUID for {gamertag} is {xuid}")

        elif option == "Ban XUID":
            st.subheader("Ban XUID")
            xuid = st.text_input("Enter XUID to ban")
            if st.button("Confirm Ban"):
                st.success(f"XUID {xuid} banned!")

        elif option == "Spam Messages":
            st.subheader("Spam Messages")
            gamertag = st.text_input("Gamertag to spam")
            message = st.text_area("Message")
            count = st.number_input("Number of messages", min_value=1)
            if st.button("Start Spam"):
                with st.spinner('Spamming...'):
                    asyncio.run(spam_messages(gamertag, message, int(count)))
                st.success("Spam sent!")

        elif option == "Report Spammer":
            st.subheader("Report Spammer")
            gamertag = st.text_input("Gamertag to report")
            report_message = st.text_area("Report message")
            count = st.number_input("Number of reports", min_value=1)
            if st.button("Send Reports"):
                with st.spinner('Reporting...'):
                    asyncio.run(report_spammer(gamertag, report_message, int(count)))
                st.success("Reports sent!")

        elif option == "Logout":
            st.session_state['logged_in'] = False
            st.session_state['user'] = ""
            st.experimental_rerun()

# Call main() if script is run directly
if __name__ == "__main__":
    main()
