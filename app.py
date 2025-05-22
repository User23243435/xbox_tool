import streamlit as st
import asyncio
import json
import os
import random

# Define your background URL
BACKGROUND_URL = "https://images.unsplash.com/photo-1506744038136-46273834b3fb"  # or your preferred background image

# --- Inject background CSS only once ---
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
        /* Optional overlay for contrast */
        /* .overlay {{
            background-color: rgba(0,0,0,0.3);
            position: fixed;
            top:0; left:0; width:100%; height:100%;
            z-index: -1;
        }} */
        </style>
        """, unsafe_allow_html=True
    )
    st.session_state['bg_injected'] = True

# --- Your header or logo (if any) --- 
# For example, if you want a header image, include it here
# st.markdown(your_header_html, unsafe_allow_html=True)

# --- Your app logic ---
def main():
    # Load or create users data
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            users = json.load(f)
    else:
        users = {}

    # init session state
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'user' not in st.session_state:
        st.session_state['user'] = ''

    # Authentication flow
    if not st.session_state['logged_in']:
        choice = st.radio("Create account or login:", ["Login", "Register"])
        if choice == "Login":
            login()
        else:
            register()
        if not st.session_state['logged_in']:
            return

    # Main menu
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

# --- Your login and register functions ---
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

# --- Your async functions (convert, spam, report) ---
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

# --- Run the app ---
if __name__ == "__main__":
    main()
