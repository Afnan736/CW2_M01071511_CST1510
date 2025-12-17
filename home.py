import streamlit as st
import bcrypt
from app.user import check_username_exists, add_user,get_user_hash,change_username,change_password,delete_user_account
from application import validate_password_strength


# Page configuration - sets up the web page layout
st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")
st.header("Login & Registration")  # Main page title

# Create two tabs for Login and Registration functionality
tab1, tab2 = st.tabs(["Login", "Register"])

# LOGIN TAB - handles user authentication and account management
with tab1:
    # Login form inputs
    user = st.text_input("Username", key="login_user")
    pwd = st.text_input("Password", type="password", key="login_pwd")

    # Login button logic
    if st.button("Login", key="login_btn"):
        hash_val = get_user_hash(user)  # Retrieve stored password hash for user
        
        # Verify password against stored hash
        if hash_val and bcrypt.checkpw(pwd.encode(), hash_val.encode()):
            # Set session state to track logged-in user
            st.session_state["logged_in"] = True
            st.session_state["username"] = user
            st.success("Logged in successfully")
            st.switch_page("pages/Cyber_Incident.py")  # Redirect to main app page
        else:
            st.error("Invalid username or password")  # Authentication failed

    # EXPANDER: Change Username or Password - for account modifications
    with st.expander("Change Username or Password"):
        # Username change section
        old = st.text_input("Old Username", key="change_old_user")
        new = st.text_input("New Username", key="change_new_user")

        if st.button("Change Username", key="change_user_btn"):
            # Validate old username exists and new username is available
            if not check_username_exists(old):
                st.error("Old username not found")
            elif check_username_exists(new):
                st.error("New username already exists")
            else:
                change_username(old, new)  # Update username in database
                st.success("Username changed successfully")

        st.divider()  # Visual separator

        # Password change section
        user_pass = st.text_input(
            "Username for Password Change", key="change_pass_user"
        )
        new_pass = st.text_input(
            "New Password", type="password", key="change_new_pass"
        )

        if st.button("Change Password", key="change_pass_btn"):
            # Validate password strength requirements
            valid, missing = validate_password_strength(new_pass)

            if not check_username_exists(user_pass):
                st.error("Username not found")
            elif not valid:
                # Display specific password requirements not met
                st.error("Password does not meet requirements:")
                for req in missing:
                    st.write(f"- {req}")
            else:
                # Hash new password and update in database
                new_hash = bcrypt.hashpw(
                    new_pass.encode(), bcrypt.gensalt()
                ).decode()
                change_password(user_pass, new_hash)
                st.success("Password changed successfully")

    # EXPANDER: Delete Account - for account deletion with confirmation
    with st.expander("Delete Account"):
        del_user = st.text_input("Username", key="del_user")
        del_pwd = st.text_input("Password", type="password", key="del_pwd")
        confirm = st.text_input('Type "DELETE" to confirm', key="del_confirm")

        if st.button("Delete Account", key="del_btn"):
            # Multi-step verification for account deletion
            if not check_username_exists(del_user):
                st.error("Username not found")
            else:
                hash_val = get_user_hash(del_user)
                # Verify password is correct
                if not hash_val or not bcrypt.checkpw(
                    del_pwd.encode(), hash_val.encode()
                ):
                    st.error("Incorrect password")
                # Require explicit confirmation text
                elif confirm != "DELETE":
                    st.error('You must type "DELETE" to confirm')
                else:
                    delete_user_account(del_user)  # Remove user from database
                    st.success(f"Account '{del_user}' deleted successfully")

# REGISTER TAB - handles new user registration
with tab2:
    # Registration form inputs
    new_user = st.text_input("New Username", key="reg_user")
    new_pwd = st.text_input("New Password", type="password", key="reg_pwd")

    if st.button("Register", key="reg_btn"):
        # Validate password meets security requirements
        valid, missing = validate_password_strength(new_pwd)

        if not valid:
            # Show which password requirements failed
            st.error("Password does not meet requirements:")
            for req in missing:
                st.write(f"- {req}")
        elif check_username_exists(new_user):
            st.error("Username already exists")  # Username uniqueness check
        else:
            # Hash password and create new user account
            hash_val = bcrypt.hashpw(
                new_pwd.encode(), bcrypt.gensalt()
            ).decode()
            add_user(new_user, hash_val)  # Add user to database
            st.success("Registered successfully!")