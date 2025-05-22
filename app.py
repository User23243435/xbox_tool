import streamlit as st
import json
import os
import asyncio
import random

# --- Set page config ---
st.set_page_config(page_title="Xbox Tool", layout="centered")

# --- Embed background video with correct styling ---
st.markdown(
    """
    <style>
    /* Make the background video fill the page and stay in the back */
    .background-video {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        z-index: -1;
    }
    /* Make sure all content appears above the video */
    .content {
        position: relative;
        z-index: 1;
        padding: 20px;
        color: #fff;
    }
    /* Style your header image */
    img.header-img {
        width: 50%;
        max-width: 350px;
        height: auto;
        display: block;
        margin: 10px auto;
        z-index: 1; /* ensure it appears above the video */
    }
    </style>
    <video autoplay loop muted playsinline class="background-video">
        <source src="https://res.cloudinary.com/dnctrdcuk/video/upload/v1747890083/xwu9dwpagrqlbvhd8dov.mp4" type="video/mp4" />
    </video>
    """,
    unsafe_allow_html=True
)

# --- Your existing header image ---
header_image_url = "https://i.imgur.com/WhRBcgw.png"
st.markdown(
    f'<img src="{header_image_url}" class="header-img" alt="XBOX TOOL">',
    unsafe_allow_html=True
)

# --- Hide default Streamlit UI elements ---
st.markdown(
    """
    <style>
    header {display: none !important;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stHelpSidebar"] {display: none;}
    @media (max-width: 768px) {
        img.header-img { width: 70% !important; }
        h1, h2, h3, h4, h5, h6 { font-size: calc(1.2em + 1vw) !important; }
        .block-container { flex-direction: column !important; }
        button, input[type=text], input[type=password], textarea, input[type=number] {
            width: 100% !important; font-size: 1.2em; padding: 12px;
        }
        .css-1d391kg { padding: 10px !important; }
        img { max-width: 80% !important; height: auto !important; }
    }
    </style>
    """,
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

# Async functions (simulate API)
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

# Main app
def main():
    if not st.session_state['logged_in']:
        choice = st.radio("Create account or login:", ["Login", "Register"])
        if choice == "Login":
            login()
        else:
            register()
        return

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
            # Here you'd add the ban logic
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

if __name__ == "__main__":
    main()
