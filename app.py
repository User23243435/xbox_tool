import streamlit as st
import json
import os
import asyncio
import random

# --- Hide Streamlit default menu, header, footer, and top icons ---
st.set_page_config(page_title="Xbox Tool", layout="centered")
st.markdown(
    """
    <style>
    /* Hide header, menu, footer */
    header {display: none !important;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stHelpSidebar"] {display: none;}

    /* Responsive styles for mobile devices */
    @media (max-width: 768px) {
        /* Make header image smaller and centered */
        img.header-img {
            width: 70% !important;
        }
        /* Make main header text larger for readability */
        h1, h2, h3, h4, h5, h6 {
            font-size: calc(1.2em + 1vw) !important;
        }
        /* Stack columns vertically instead of side by side */
        .block-container {
            flex-direction: column !important;
        }
        /* Make buttons and inputs full width */
        button, input[type=text], input[type=password], textarea, input[type=number] {
            width: 100% !important;
            font-size: 1.2em;
            padding: 12px;
        }
        /* Adjust margins/padding for better mobile fit */
        .css-1d391kg {
            padding: 10px !important;
        }
        /* Make images scale down */
        img {
            max-width: 80% !important;
            height: auto !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Embed your header image ---
header_image_url = "https://i.imgur.com/WhRBcgw.png"

# --- Apply background CSS ---
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
    /* Make images with class 'header-img' responsive */
    img.header-img {
        width: 50%;
        max-width: 350px;
        height: auto;
        display: block;
        margin: 10px auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Show your smaller "XBOX TOOL" header (words only) ---
st.markdown(
    f'<img src="{header_image_url}" class="header-img" alt="XBOX TOOL">',
    unsafe_allow_html=True
)

# --- Load or initialize users data ---
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

# --- Session state for login ---
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

    # Main interface
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
