import streamlit as st
import os
import json
import requests

# Set page config - must be the first Streamlit command
st.set_page_config(page_title="Xbox Tool", page_icon="🎮")

# Custom background and style
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

# Header Image
st.markdown(
    '<div style="text-align:center;">'
    '<img src="https://i.imgur.com/uAQOm2Y.png" style="width:600px; max-width:90%; height:auto; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">'
    '</div>',
    unsafe_allow_html=True
)

# Load existing user data
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)

if os.path.exists("user_keys.json"):
    with open("user_keys.json", "r") as f:
        user_keys = json.load(f)
else:
    user_keys = {}  # username: api_key

def save_keys():
    with open("user_keys.json", "w") as f:
        json.dump(user_keys, f)

# -------- Step 1: Input XboxAPI Key --------
st.title("Enter Your XboxAPI Key")
api_key = st.text_input("Your XboxAPI Key")

if st.button("Save API Key") and api_key:
    # Save under a temporary user; will be associated after login
    temp_username = "tempuser"
    user_keys[temp_username] = api_key
    save_keys()
    st.success("API key saved. Please register or login.")
    st.session_state['api_key_saved'] = True

# -------- Step 2: Register/Login --------
if st.session_state.get('api_key_saved'):
    if 'current_user' not in st.session_state:
        st.session_state['current_user'] = None

    if st.session_state['current_user'] is None:
        # Show Register/Login form
        st.title("Register or Login")
        mode = st.radio("Mode", ["Login", "Register"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Submit"):
            if mode == "Register":
                if username in users:
                    st.error("Username already exists")
                else:
                    users[username] = {'password': password}
                    save_users()
                    st.success("Registration successful. Please login.")
            else:
                if username in users and users[username]['password'] == password:
                    st.session_state['current_user'] = username
                    # Save API key if provided now
                    if 'api_key' in locals() and api_key:
                        user_keys[username] = api_key
                        save_keys()
                    st.success(f"Logged in as {username}")
                else:
                    st.error("Invalid username or password")
        st.stop()

    # User is logged in
    username = st.session_state['current_user']
    user_api_key = user_keys.get(username, '')

    # If no API key stored, prompt to add
    if not user_api_key:
        st.markdown("**Click here if you don't have an API key:**")
        st.markdown("[Get your Xbox API Key](https://xbl.io/console)")
        new_key = st.text_input("Enter your XboxAPI key")
        if st.button("Save API Key") and new_key:
            # Validate the API key
            def validate_api_key(key):
                # Make a test API request to validate
                headers = {'X-Auth': key}
                try:
                    response = requests.get("https://xbl.io/api/v5/users/xuid/1234567890", headers=headers)
                    if response.status_code == 200:
                        return True
                except:
                    pass
                return False

            if validate_api_key(new_key):
                users[username] = {'password': users[username]['password']}
                user_keys[username] = new_key
                save_users()
                save_keys()
                st.success("API key validated and saved.")
                user_api_key = new_key
            else:
                st.error("Invalid API Key. Please check and try again.")
        st.stop()

    # Proceed if API key is available
    if user_api_key:
        # Show main menu
        action = st.radio("Select an action:", [
            "Convert Gamertag to XUID",
            "Ban XUID",
            "Spam Messages",
            "Report Spammer",
            "Logout"
        ])

        def make_api_call(endpoint, params=None):
            # Replace with actual API request
            headers = {'X-Auth': user_api_key}
            # Example: response = requests.get(f"https://xbl.io/api/{endpoint}", headers=headers, params=params)
            return {"status": "success", "data": "Fake data"}

        def convert_gamertag():
            gamertag = st.text_input("Gamertag")
            if st.button("Convert"):
                result = make_api_call("convert_gamertag", {'gamertag': gamertag})
                st.success(f"Simulated XUID: 1234567890 for {gamertag}")

        def ban_xuid():
            xuid = st.text_input("XUID to ban")
            if st.button("Ban XUID"):
                make_api_call("ban_xuid", {'xuid': xuid})
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
