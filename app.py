import streamlit as st
import os
import json

# Basic page setup
st.set_page_config(page_title="Xbox Tool", page_icon="🎮")
st.markdown(
    '<link rel="apple-touch-icon" href="https://i.imgur.com/27Wxhe3.png" />',
    unsafe_allow_html=True
)
st.markdown("""
    <style>
    body { margin:0; padding:0; }
    .stApp {
        margin-top:0; padding-top:0;
        background-image: url("https://4kwallpapers.com/images/wallpapers/neon-xbox-logo-2880x1800-13434.png");
        background-size: cover; background-position: center; background-repeat: no-repeat; min-height: 100vh;
    }
    header { display:none !important; }
    #MainMenu { visibility:hidden; }
    footer { visibility:hidden; }
    div[data-testid="stHelpSidebar"] { display:none; }
    </style>
""")

# Load user data
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)

# Load user API keys
if os.path.exists("user_keys.json"):
    with open("user_keys.json", "r") as f:
        user_keys = json.load(f)
else:
    user_keys = {}  # username: api_key

def save_keys():
    with open("user_keys.json", "w") as f:
        json.dump(user_keys, f)

# User Registration/Login
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None

if st.session_state['current_user'] is None:
    st.title("Register or Login")
    mode = st.radio("Mode", ["Login", "Register"])
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")
    if st.button("Submit"):
        if mode == "Register":
            if username_input in users:
                st.error("Username exists.")
            else:
                users[username_input] = password_input
                save_users()
                st.success("Registered! Please login.")
        else:
            if username_input in users and users[username_input] == password_input:
                st.session_state['current_user'] = username_input
                st.success(f"Logged in as {username_input}")
            else:
                st.error("Invalid login.")
    st.stop()

# User is logged in
current_user = st.session_state['current_user']

# If logged in, ask for API key
if current_user:
    if current_user not in user_keys:
        st.info("Enter your XboxAPI.com API key to use the service.")
        api_key_input = st.text_input("Your XboxAPI Key")
        if st.button("Save API Key") and api_key_input:
            user_keys[current_user] = api_key_input
            save_keys()
            st.success("API key saved.")
    else:
        api_key_input = user_keys[current_user]
        st.write(f"API key loaded for {current_user}")

# Main menu
action = st.radio("Select an action:", [
    "Convert Gamertag to XUID",
    "Ban XUID",
    "Spam Messages",
    "Report Spammer",
    "Logout"
])

# Example function to call XboxAPI with stored key
def make_api_call(endpoint, params=None):
    key = api_key_input
    headers = {'X-Auth': key}
    # insert your actual API request here
    # response = requests.get("https://xboxapi.com/v2/endpoint", headers=headers, params=params)
    # return response.json()
    return {"status": "success", "data": "Fake data"}

# Example actions
def convert_gamertag():
    gamertag = st.text_input("Enter Gamertag")
    if st.button("Convert"):
        result = make_api_call("convert_gamertag")  # replace with real API call
        st.success(f"Simulated XUID for {gamertag}: 1234567890")

def ban_xuid():
    xuid = st.text_input("Enter XUID to ban")
    if st.button("Confirm Ban"):
        make_api_call("ban_xuid")
        st.success(f"XUID {xuid} banned.")

def spam_messages():
    gamertag = st.text_input("Gamertag to spam")
    message = st.text_area("Message")
    count = st.number_input("Number of messages", min_value=1)
    if st.button("Start Spam"):
        for _ in range(int(count)):
            pass
        st.success("Spam sent!")

def report_spammer():
    gamertag = st.text_input("Gamertag to report")
    report_message = st.text_area("Report message")
    count = st.number_input("Number of reports", min_value=1)
    if st.button("Send Reports"):
        for _ in range(int(count)):
            pass
        st.success("Reports sent!")

def logout():
    st.session_state['current_user'] = None
    st.experimental_rerun()

# Run selected action
if action == "Convert Gamertag to XUID":
    convert_gamertag()
elif action == "Ban XUID":
    ban_xuid()
elif action == "Spam Messages":
    spam_messages()
elif action == "Report Spammer":
    report_spammer()
elif action == "Logout":
    logout()
