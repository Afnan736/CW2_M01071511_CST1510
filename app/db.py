import sqlite3

def get_connection():
    """Get connection to the SQLite database"""
    # Create database connection
    conn = sqlite3.connect('DATA/intelligence_platform.db', check_same_thread=False)
    return conn