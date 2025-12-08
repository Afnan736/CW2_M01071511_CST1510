import sqlite3
from app.db import get_connection

# 1. CHECK USERNAME
def check_username_exists(username):
    conn = get_connection()
    curr = conn.cursor()
    curr.execute("SELECT COUNT(*) FROM users WHERE Username = ?", (username,))
    result = curr.fetchone()
    conn.close()
    return result[0] > 0 if result else False

# 2. ADD USER
def add_user(username, password, hash_password):  
    conn = get_connection()
    curr = conn.cursor()
    curr.execute("INSERT INTO users (Username, Password, Password_hash) VALUES (?, ?, ?)", 
                (username, password, hash_password))
    conn.commit()
    conn.close()

# 3. CHANGE USERNAME
def change_username(old_name, new_name):
    conn = get_connection()
    curr = conn.cursor()
    curr.execute("UPDATE users SET Username = ? WHERE Username = ?", (new_name, old_name))
    conn.commit()
    conn.close()

# 4. CHANGE PASSWORD
def change_password(username, new_password, new_hash):
    conn = get_connection()
    curr = conn.cursor()
    curr.execute("UPDATE users SET Password = ?, Password_hash = ? WHERE Username = ?", 
                (new_password, new_hash, username))
    conn.commit()
    conn.close()

# 5. GET ALL USERS
def get_all_users():
    conn = get_connection()  
    curr = conn.cursor()
    curr.execute("SELECT * FROM users")
    users = curr.fetchall()
    conn.close()
    return users

# 6. DELETE USER ACCOUNT - NEW
def delete_user_account(username):
    """Delete user account - removes username, password and hashed password"""
    conn = get_connection()
    curr = conn.cursor()
    # This deletes EVERYTHING for that user
    curr.execute("DELETE FROM users WHERE Username = ?", (username,))
    conn.commit()
    conn.close()



def get_user_hash(username):
   
    conn = get_connection()
    curr = conn.cursor()
    curr.execute("SELECT Password_hash FROM users WHERE Username = ?", (username,))
    result = curr.fetchone()
    conn.close()
    return result[0] if result else None

