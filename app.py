import streamlit as st
import os
import asyncio
import json
import random

# 1. Set page title and emoji icon (browser tab)
st.set_page_config(
    page_title="Xbox Tool",
    page_icon="🎮"
)

# 2. Add your custom icon for iOS (replace with your PNG URL)
st.markdown(
    '<link rel="apple-touch-icon" href="https://i.imgur.com/sZMG8WG.png" />',
    unsafe_allow_html=True
)

# 3. Remove default margins/padding to fix top white border & set background
st.markdown(
    """
    <style>
    body {
        margin: 0;
        padding: 0;
    }
    .stApp {
        margin-top: 0;
        padding-top: 0;
        background-image: url("https://4kwallpapers.com/images/wallpapers/neon-xbox-logo-2880x1800-13434.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        min-height: 100vh;
    }
    /* Hide default menu and footer for a cleaner look */
    header {display: none !important;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stHelpSidebar"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True
)

# 4. Header image
st.markdown(
    '<div style="text-align:center;">'
    '<img src="https://i.imgur.com/uAQOm2Y.png" style="width:600px; max-width:90%; height:auto; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">'
    '</div>',
    unsafe_allow_html=True
)

# --- Your login/register logic now ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = ''

# Load users
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)

def generate_captcha():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    return f"What is {a} + {b}?", a + b

def show_alert(text):
    # Show text inside an orange box (like error message)
    st.markdown(
        f'<div style="background-color:#FFA500; padding:10px; border-radius:5px;">{text}</div>',
        unsafe_allow_html=True
    )

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
            show_alert("🛑 Wrong captcha")
        elif username in users and users[username] == password:
            st.session_state['logged_in'] = True
            st.session_state['user'] = username
            st.success(f"✅ Welcome {username}!")
            q, a = generate_captcha()
            st.session_state['captcha_q'], st.session_state['captcha_a'] = q, a
        else:
            show_alert("🛑 Wrong username or password")
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
            show_alert("🛑 Username exists")
        elif password != confirm:
            show_alert("🛑 Passwords don't match")
        elif captcha_input != str(st.session_state['captcha_a']):
            show_alert("🛑 Wrong captcha")
        elif not password:
            show_alert("🛑 Password cannot be empty")
        else:
            users[username] = password
            save_users()
            st.success("✅ Registered! Please login.")
            q, a = generate_captcha()
            st.session_state['captcha_q'], st.session_state['captcha_a'] = q, a

# Main app logic
if not st.session_state['logged_in']:
    choice = st.radio("Create account or login:", ["Login", "Register"])
    if choice == "Login":
        login()
    else:
        register()
    if not st.session_state['logged_in']:
        st.stop()

# Main menu options
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
        # Simulate async call
        xuid = asyncio.run(asyncio.sleep(1, result="1234567890"))
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
        # simulate spam
        for _ in range(int(count)):
            pass
        st.success("Spam sent!")

elif option == "Report Spammer":
    gamertag = st.text_input("Gamertag to report")
    report_message = st.text_area("Report message")
    count = st.number_input("Number of reports", min_value=1)
    if st.button("Send Reports"):
        # simulate report
        for _ in range(int(count)):
            pass
        st.success("Reports sent!")

elif option == "Logout":
    st.session_state['logged_in'] = False
    st.session_state['user'] = ""
    st.experimental_rerun()
