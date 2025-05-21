import streamlit as st

# Predefined users (for demo purposes)
users = {
    "user1": "password1",
    "user2": "password2"
}

def main():
    st.title("Secure App with User Registration & CAPTCHA")
    st.write("Please log in or register to access the app.")

    # Tabs for Login and Register
    login_or_register = st.radio("Choose an option:", ["Login", "Register"])

    if login_or_register == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        not_a_robot = st.checkbox("I'm not a robot")

        if st.button("Login"):
            if username in users and users[username] == password and not_a_robot:
                st.success(f"Welcome, {username}!")
                # Your app content here
                st.write("This is the protected app content.")
            else:
                if not username or not password:
                    st.warning("Please enter username and password.")
                elif not_a_robot:
                    st.error("Invalid credentials or verification failed.")
                else:
                    st.warning("Please verify you're not a robot.")
    else:
        # Registration
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        register_not_a_robot = st.checkbox("I'm not a robot (Register)")

        if st.button("Register"):
            if not new_username or not new_password or not confirm_password:
                st.warning("Please fill out all fields.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            elif new_username in users:
                st.warning("Username already exists.")
            elif not register_not_a_robot:
                st.warning("Please verify you're not a robot.")
            else:
                # Save new user (here, just updating the dict)
                users[new_username] = new_password
                st.success("Registration successful! You can now log in.")

if __name__ == "__main__":
    main()