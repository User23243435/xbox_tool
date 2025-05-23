import streamlit as st
import os
import json

# Style for background and hiding headers
st.set_page_config(page_title="Xbox Tool", page_icon="🎮")
st.markdown(
    """
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
    """,
    unsafe_allow_html=True
)

# Header
st.markdown(
    '<div style="text-align:center;">'
    '<img src="https://i.imgur.com/uAQOm2Y.png" style="width:600px; max-width:90%; height:auto; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">'
    '</div>',
    unsafe_allow_html=True
)

# Load user data
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)

# User registration/login
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None

if st.session_state['current_user'] is None:
    # Register/Login
    st.title("Register or Login")
    mode = st.radio("Mode", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    api_key = st.text_input("Your XboxAPI Key (or leave blank to add later)")
    if st.button("Submit"):
        if mode == "Register":
            if username in users:
                st.error("Username exists.")
            else:
                users[username] = {'password': password, 'api_key': api_key}
                save_users()
                st.success("Registration complete. Please login.")
        else:
            if username in users and users[username]['password'] == password:
                st.session_state['current_user'] = username
                # Save API key if provided during login
                if api_key:
                    users[username]['api_key'] = api_key
                    save_users()
                st.success(f"Logged in as {username}")
            else:
                st.error("Invalid login.")
    st.stop()

# Logged in user
username = st.session_state['current_user']
user_data = users.get(username, {})
user_api_key = user_data.get('api_key', '')

# Prompt to add API key if missing
if not user_api_key:
    st.info("You need an Xbox API key to use the features.")
    st.markdown("Get your API key at [https://xbl.io/console](https://xbl.io/console)")
    new_key = st.text_input("Enter your XboxAPI key")
    if st.button("Save API Key") and new_key:
        users[username]['api_key'] = new_key
        save_users()
        st.success("API key saved.")
        user_api_key = new_key

# Now, with API key available, show main menu
if user_api_key:
    action = st.radio("Select an action:", [
        "Convert Gamertag to XUID",
        "Ban XUID",
        "Spam Messages",
        "Report Spammer",
        "Logout"
    ])

    def make_api_call(endpoint, params=None):
        # replace with real API request
        headers = {'X-Auth': user_api_key}
        # response = requests.get(f"https://xbl.io/api/{endpoint}", headers=headers, params=params)
        # return response.json()
        return {"status": "success", "data": "Fake data"}

    def convert_gamertag():
        gamertag = st.text_input("Gamertag")
        if st.button("Convert"):
            result = make_api_call("whatever_endpoint", {'gamertag': gamertag})
            st.success(f"Simulated XUID: 1234567890 for {gamertag}")

    def ban_xuid():
        xuid = st.text_input("XUID to ban")
        if st.button("Ban XUID"):
            make_api_call("ban_endpoint", {'xuid': xuid})
            st.success(f"Banned XUID {xuid}")

    def spam_messages():
        gamertag = st.text_input("Gamertag to spam")
        message = st.text_area("Message")
        count = st.number_input("Number of messages", min_value=1)
        if st.button("Spam"):
            for _ in range(int(count)):
                pass
            st.success("Spam sent!")

    def report_spammer():
        gamertag = st.text_input("Gamertag to report")
        report_message = st.text_area("Report message")
        count = st.number_input("Number of reports", min_value=1)
        if st.button("Send reports"):
            for _ in range(int(count)):
                pass
            st.success("Reports sent!")

    def logout():
        st.session_state['current_user'] = None
        st.experimental_rerun()

    # Run the selected action
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
