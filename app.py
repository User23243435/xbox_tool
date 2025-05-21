import streamlit as st
import json
import os
import asyncio
import random

# Background image URL
background_url = "https://4kwallpapers.com/images/wallpapers/xbox-logo-black-background-amoled-gradient-5k-1920x1200-3285.png"

# Image URL to replace ASCII art
header_image_url = "https://see.fontimg.com/api/rf5/1GyyM/NzI4MWVlYTljMmQ0NGViM2IyOTc1MmIzNWE2ODYwNzYub3Rm/WEJPWCBUT09M/milkywaypersonaluse-bold.png?r=dw&h=65&w=1000&fg=000000&bg=FFFFFF&s=65"

# Apply background CSS
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
    </style>
    """, unsafe_allow_html=True
)

# Embed header image
st.markdown(
    f"""
    <img src="{header_image_url}" style="width: 100%; max-width: 1000px; height: 65px; object-fit: contain; display: block; margin: 0 auto;"/>
    """, unsafe_allow_html=True
)

# Load or initialize users data
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

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

# Registration
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

# Login
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

# Dummy async functions
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

# Main
def main():
    if not st.session_state['logged_in']:
        choice = st.radio("Create account or login:", ["Login", "Register"])
        if choice == "Login":
            login()
        else:
            register()
        return

    # Optional: a small header or message
    # (You can remove or replace this if you want)
    # Small header already included above as image.

    # Your main interface
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🛡️ Ban XUID"):
            xuid = st.text_input("Enter XUID to ban")
            if st.button("✅ Confirm Ban"):
                st.success(f"XUID {xuid} banned!")
    with col2:
        if st.button("📩 Spam Messages"):
            gamertag = st.text_input("Gamertag to spam")
            message = st.text_area("Message")
            count = st.number_input("Number of messages", min_value=1)
            if st.button("🚀 Start Spam"):
                asyncio.run(spam_messages(gamertag, message, int(count)))
                st.success("Spam sent!")

    if st.button("🚨 Report Spammer"):
        gamertag = st.text_input("Gamertag to report")
        report_message = st.text_area("Report message")
        count = st.number_input("Number of reports", min_value=1)
        if st.button("📝 Send Reports"):
            asyncio.run(report_spammer(gamertag, report_message, int(count)))
            st.success("Reports sent!")

    if st.button("🔓 Logout"):
        st.session_state['logged_in'] = False
        st.session_state['user'] = ""
        st.experimental_rerun()

if __name__ == "__main__":
    main()
