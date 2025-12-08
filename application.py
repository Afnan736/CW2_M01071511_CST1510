import bcrypt
import string
# Add get_user_hash to the imports
from app.user import check_username_exists, add_user, change_username, change_password, delete_user_account, get_user_hash

def hash_password(password):
    binary_pass = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(binary_pass, salt)
    return hashed_password.decode('utf-8')

def validate_hash(password, stored_hash):
    hash_bytes = stored_hash.encode('utf-8')
    password_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hash_bytes)

def validate_password_strength(psw):
    has_upper = any(char.isupper() for char in psw)
    has_lower = any(char.islower() for char in psw)
    has_digit = any(char.isdigit() for char in psw)
    has_special = any(char in string.punctuation for char in psw)
    has_space = ' ' in psw
    
    if len(psw) >= 8 and has_upper and has_lower and has_digit and has_special and not has_space:
        return True
    else:
        print("Password must have:")
        print("- At least 8 characters" if len(psw) >= 8 else "- Minimum 8 characters")
        print("- Uppercase letter" if has_upper else "- At least one uppercase letter")
        print("- Lowercase letter" if has_lower else "- At least one lowercase letter")
        print("- Number" if has_digit else "- At least one number")
        print("- Special character" if has_special else "- At least one special character")
        print("- No spaces" if not has_space else "- Remove spaces")
        return False

def register_user():
    # Username validation
    while True:
        username = input('Enter your username: ').strip()
        
        if not username:
            print("Username cannot be empty.")
            continue
            
        if len(username) < 3 or len(username) > 20:
            print("Username must be between 3 and 20 characters.")
            continue
            
        if ' ' in username:
            print("Username cannot contain spaces.")
            continue

        # Check if username already exists
        if check_username_exists(username):
            print("Username already exists. Please choose a different username.")
            continue
        else:
            break 

    # Password validation
    while True:
        psw = input('Enter your password: ')
        if not psw:
            print("Password cannot be empty.")
            continue
            
        if validate_password_strength(psw):
            break
        continue
    
    hash_val = hash_password(psw)
    
    # Save to database
    add_user(username, psw, hash_val)
    
    print("Registered successfully!")

def change_username_menu():
    """Change username function"""
    old_username = input("Enter your current username: ").strip()
    
    # Check if old username exists
    if not check_username_exists(old_username):
        print(f"User '{old_username}' not found.")
        return
    
    # Get new username
    while True:
        new_username = input("Enter new username: ").strip()
        
        if not new_username:
            print("Username cannot be empty.")
            continue
            
        if len(new_username) < 3 or len(new_username) > 20:
            print("Username must be between 3 and 20 characters.")
            continue
            
        if ' ' in new_username:
            print("Username cannot contain spaces.")
            continue
            
        if check_username_exists(new_username):
            print("Username already exists. Please choose a different one.")
            continue
            
        break
    
    # Change username
    change_username(old_username, new_username)
    print(f"Username changed from '{old_username}' to '{new_username}'")

def change_password_menu():
    """Change password function"""
    username = input("Enter your username: ").strip()
    
    # Check if user exists
    if not check_username_exists(username):
        print(f"User '{username}' not found.")
        return
    
    # Get new password
    while True:
        new_psw = input("Enter new password: ")
        confirm_psw = input("Confirm new password: ")
        
        if new_psw != confirm_psw:
            print("Passwords don't match. Try again.")
            continue
            
        if validate_password_strength(new_psw):
            break
        continue
    
    # Hash and update password
    new_hash = hash_password(new_psw)
    change_password(username, new_psw, new_hash)
    print(f"Password changed for '{username}'")

def delete_account_menu():
    """Delete account function"""
    username = input("Enter username to delete: ").strip()
    
    # Check if user exists
    if not check_username_exists(username):
        print(f"User '{username}' not found.")
        return
    
    # Ask for password
    password = input("Enter password to confirm deletion: ")
    
    # Verify password
    stored_hash = get_user_hash(username)
    if not stored_hash or not validate_hash(password, stored_hash):
        print("Incorrect password. Deletion cancelled.")
        return
    
    # Confirm deletion
    confirm = input(f"Are you sure you want to delete '{username}'? Type 'yes' to confirm: ").strip().lower()
    
    if confirm == 'yes':
        delete_user_account(username)
        print(f"User '{username}' deleted. Username, password and hashed password removed.")
    else:
        print("Deletion cancelled.")


def log_in():
    """Login function"""
    while True:
        username = input('Enter your username: ').strip()
        password = input('Enter your password: ')

        # Get hash from database using function in user.py
        stored_hash = get_user_hash(username)
        
        if stored_hash:
            if validate_hash(password, stored_hash):
                print("Login successful!")
                return True
            else:
                print("Wrong password. Try again.")
                break
        else:
            print('Username not found. Try again.')
            return False