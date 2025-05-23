import streamlit as st
import os
import json
import requests

# --- 1. Set page config (must be first) ---
st.set_page_config(page_title="Xbox Tool", page_icon="🎮")

# --- 2. Custom style ---
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

# --- 3. Header image ---
st.markdown(
    '<div style="text-align:center;">'
    '<img src="https://i.imgur.com/uAQOm2Y.png" style="width:600px; max-width:90%; height:auto; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">'
    '</div>',
    unsafe_allow_html=True
)

# --- 4. Load data ---
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
    user_keys = {}

def save_keys():
    with open("user_keys.json", "w") as f:
        json.dump(user_keys, f)

# --- 5. Validation function ---
def validate_api_key(api_key):
    url = "https://xbl.io/api/v5/account/ownership"
    headers = {'X-Auth': api_key}
    try:
        response = requests.get(url, headers=headers)
        return response.status_code == 200
    except:
        return False

# --- 6. Manage login state ---
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None
if 'api_key_valid' not in st.session_state:
    st.session_state['api_key_valid'] = False

# --- 7. Check if user has a valid saved API key ---
if st.session_state['current_user']:
    current_user = st.session_state['current_user']
    user_api_key = user_keys.get(current_user, '')
    # Validate stored key
    if user_api_key:
        if validate_api_key(user_api_key):
            st.session_state['api_key_valid'] = True
        else:
            # Invalid key, reset session
            st.session_state['current_user'] = None
            st.session_state['api_key_valid'] = False

# --- 8. If no valid API key, prompt for it ---
if not st.session_state['api_key_valid']:
    # Show link and input
    st.markdown("### Click here if you don't have an API key:")
    st.markdown("[Get your Xbox API Key](https://xbl.io/console)")
    new_key = st.text_input("Enter your XboxAPI key here")
    if st.button("Save API Key") and new_key:
        # Validate key
        if validate_api_key(new_key):
            # Save as temporary user
            temp_username = "tempuser"
            user_keys[temp_username] = new_key
            save_keys()
            st.session_state['current_user'] = temp_username
            st.success("API Key validated! Please register or login.")
            st.experimental_rerun()
        else:
            st.error("Invalid API Key. Please check and try again.")
    st.stop()

# --- 9. Registration/Login flow for tempuser ---
if st.session_state['current_user']:
    current_user = st.session_state['current_user']
    user_api_key = user_keys.get(current_user, '')

    # If user is "tempuser", show register/login form
    if current_user == 'tempuser' and user_api_key:
        st.title("Register or Login")
        mode = st.radio("Mode", ["Login", "Register"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Submit"):
            if mode == "Register":
                if username in users:
                    st.error("Username already exists.")
                else:
                    users[username] = {'password': password}
                    save_users()
                    # Save API key to this username
                    user_keys[username] = user_api_key
                    del user_keys['tempuser']
                    save_keys()
                    st.session_state['current_user'] = username
                    st.success(f"Registered and logged in as {username}")
                    st.experimental_rerun()
            else:
                if username in users and users[username]['password'] == password:
                    # Log in
                    st.session_state['current_user'] = username
                    # Save API key to user
                    user_keys[username] = user_api_key
                    del user_keys['tempuser']
                    save_keys()
                    st.success(f"Logged in as {username}")
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password")
        st.stop()

    # --- 10. Main app interface ---
    if user_api_key:
        action = st.radio("Choose an action:", [
            "Convert Gamertag to XUID",
            "Ban XUID",
            "Spam Messages",
            "Report Spammer",
            "Logout"
        ])

        def make_api_call(endpoint, params=None):
            # Replace with actual API call
            headers = {'X-Auth': user_api_key}
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
