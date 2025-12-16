import bcrypt
import string
# Add get_user_hash to the imports
from app.user import check_username_exists, add_user, change_username, change_password, delete_user_account, get_user_hash

def hash_password(password):
    # Hash a password using bcrypt with salt
    # Convert password string to bytes for bcrypt
    binary_pass = password.encode('utf-8')
    # Generate a secure random salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(binary_pass, salt)
    # Convert bytes back to string for storage
    return hashed_password.decode('utf-8')

def validate_hash(password, stored_hash):
    # Validate a password against a stored hash
    # Convert stored hash string to bytes
    hash_bytes = stored_hash.encode('utf-8')
    # Convert input password to bytes
    password_bytes = password.encode('utf-8')
    # Use bcrypt to check if password matches hash
    return bcrypt.checkpw(password_bytes, hash_bytes)

def validate_password_strength(psw):
    # Check if password meets security requirements
    # Define all password requirements as (check_condition, error_message) tuples
    checks = [
        (len(psw) >= 8, "Minimum 8 characters"),
        (any(char.isupper() for char in psw), "At least one uppercase letter"),
        (any(char.islower() for char in psw), "At least one lowercase letter"),
        (any(char.isdigit() for char in psw), "At least one number"),
        (any(char in string.punctuation for char in psw), "At least one special character"),
        (' ' not in psw, "No spaces allowed")
    ]
    
    # Collect all failed requirements
    missing = [msg for check, msg in checks if not check]
    
    # Return success status and missing requirements
    if not missing:
        return True, []
    return False, missing

def register_user():
    # Handle new user registration
    # Username validation loop
    while True:
        username = input('Enter your username: ').strip()
        
        # Check for empty username
        if not username:
            print("Username cannot be empty.")
            continue
            
        # Check username length
        if len(username) < 3 or len(username) > 20:
            print("Username must be between 3 and 20 characters.")
            continue
            
        # Check for spaces in username
        if ' ' in username:
            print("Username cannot contain spaces.")
            continue

        # Check if username already exists in database
        if check_username_exists(username):
            print("Username already exists. Please choose a different username.")
            continue
        else:
            break  # Valid username found

    # Password validation loop
    while True:
        psw = input('Enter your password: ')
        # Check for empty password
        if not psw:
            print("Password cannot be empty.")
            continue
            
        # Validate password strength
        valid, missing = validate_password_strength(psw)
        if valid:
            break  # Password meets all requirements
        
        # Display missing requirements
        print("Missing requirements:")
        for req in missing:
            print(f"- {req}")
    
    # Hash the password for secure storage
    hash_val = hash_password(psw)
    
    # Save user to database
    add_user(username, psw, hash_val)
    
    print("Registered successfully!")

def change_username_menu():
    # Handle username change process
    # Get current username
    old_username = input("Enter your current username: ").strip()
    
    # Check if old username exists in database
    if not check_username_exists(old_username):
        print(f"User '{old_username}' not found.")
        return
    
    # New username validation loop
    while True:
        new_username = input("Enter new username: ").strip()
        
        # Check for empty new username
        if not new_username:
            print("Username cannot be empty.")
            continue
            
        # Check new username length
        if len(new_username) < 3 or len(new_username) > 20:
            print("Username must be between 3 and 20 characters.")
            continue
            
        # Check for spaces in new username
        if ' ' in new_username:
            print("Username cannot contain spaces.")
            continue
            
        # Check if new username already exists
        if check_username_exists(new_username):
            print("Username already exists. Please choose a different one.")
            continue
            
        break  # Valid new username found
    
    # Update username in database
    change_username(old_username, new_username)
    print(f"Username changed from '{old_username}' to '{new_username}'")

def change_password_menu():
    # Handle password change process
    # Get username
    username = input("Enter your username: ").strip()
    
    # Check if user exists
    if not check_username_exists(username):
        print(f"User '{username}' not found.")
        return
    
    # New password validation loop
    while True:
        new_psw = input("Enter new password: ")
        confirm_psw = input("Confirm new password: ")
        
        # Check if passwords match
        if new_psw != confirm_psw:
            print("Passwords don't match. Try again.")
            continue
            
        # Validate password strength
        valid, missing = validate_password_strength(new_psw)
        if valid:
            break  # Password meets requirements
        
        # Display missing requirements
        print("Missing requirements:")
        for req in missing:
            print(f"- {req}")
    
    # Hash the new password
    new_hash = hash_password(new_psw)
    # Update password in database
    change_password(username, new_psw, new_hash)
    print(f"Password changed for '{username}'")

def delete_account_menu():
    # Handle account deletion process
    # Get username to delete
    username = input("Enter username to delete: ").strip()
    
    # Check if user exists
    if not check_username_exists(username):
        print(f"User '{username}' not found.")
        return
    
    # Request password for verification
    password = input("Enter password to confirm deletion: ")
    
    # Get stored hash and validate password
    stored_hash = get_user_hash(username)
    if not stored_hash or not validate_hash(password, stored_hash):
        print("Incorrect password. Deletion cancelled.")
        return
    
    # Confirm deletion with explicit confirmation
    confirm = input(f"Are you sure you want to delete '{username}'? Type 'yes' to confirm: ").strip().lower()
    
    if confirm == 'yes':
        # Delete user from database
        delete_user_account(username)
        print(f"User '{username}' deleted. Username, password and hashed password removed.")
    else:
        print("Deletion cancelled.")

def log_in():
    # Handle user login process
    while True:
        # Get credentials
        username = input('Enter your username: ').strip()
        password = input('Enter your password: ')

        # Get stored hash from database
        stored_hash = get_user_hash(username)
        
        # Check if user exists
        if stored_hash:
            # Validate password against stored hash
            if validate_hash(password, stored_hash):
                print("Login successful!")
                return True
            else:
                print("Wrong password. Try again.")
                break  # Exit loop on wrong password
        else:
            print('Username not found. Try again.')
            return False  # Return False for failed login