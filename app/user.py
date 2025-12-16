import sqlite3
from app.db import get_connection  # Import database connection function

# 1. CHECK USERNAME
def check_username_exists(username):
    """Check if a username already exists in the database"""
    conn = get_connection()  # Get database connection
    curr = conn.cursor()  # Create cursor for executing SQL
    # Count users with given username
    curr.execute("SELECT COUNT(*) FROM users WHERE Username = ?", (username,))
    result = curr.fetchone()  # Get query result
    conn.close()  # Close connection
    return result[0] > 0 if result else False  # Return True if count > 0

# 2. ADD USER
def add_user(username, password, hash_password):  
    """Add a new user to the database"""
    conn = get_connection()
    curr = conn.cursor()
    # Insert new user with username, plain password, and hashed password
    curr.execute("INSERT INTO users (Username, Password, Password_hash) VALUES (?, ?, ?)", 
                (username, password, hash_password))
    conn.commit()  # Save changes to database
    conn.close()

# 3. CHANGE USERNAME
def change_username(old_name, new_name):
    """Update a user's username"""
    conn = get_connection()
    curr = conn.cursor()
    # Update username for the specified user
    curr.execute("UPDATE users SET Username = ? WHERE Username = ?", (new_name, old_name))
    conn.commit()
    conn.close()

# 4. CHANGE PASSWORD
def change_password(username, new_password, new_hash):
    """Update a user's password"""
    conn = get_connection()
    curr = conn.cursor()
    # Update both plain and hashed passwords for the user
    curr.execute("UPDATE users SET Password = ?, Password_hash = ? WHERE Username = ?", 
                (new_password, new_hash, username))
    conn.commit()
    conn.close()

# 5. GET ALL USERS
def get_all_users():
    """Retrieve all users from the database"""
    conn = get_connection()  
    curr = conn.cursor()
    curr.execute("SELECT * FROM users")  # Get all user records
    users = curr.fetchall()  # Fetch all results
    conn.close()
    return users  # Return list of user tuples

# 6. DELETE USER ACCOUNT - NEW
def delete_user_account(username):
    """Delete a user account completely from the database"""
    conn = get_connection()
    curr = conn.cursor()
    # Delete all user data for the specified username
    curr.execute("DELETE FROM users WHERE Username = ?", (username,))
    conn.commit()
    conn.close()

# 7. GET USER PASSWORD HASH
def get_user_hash(username):
    """Retrieve the hashed password for a specific user"""
    conn = get_connection()
    curr = conn.cursor()
    # Get hashed password for the username
    curr.execute("SELECT Password_hash FROM users WHERE Username = ?", (username,))
    result = curr.fetchone()  # Get single result
    conn.close()
    return result[0] if result else None  # Return hash or None if not found