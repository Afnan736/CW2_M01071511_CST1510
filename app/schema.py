import sqlite3

# Create or recreate the users table with new structure
def cte_user_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('DATA/intelligence_platform.db')  
    curr = conn.cursor()
    
    # First drop the existing table if it exists
    curr.execute("DROP TABLE IF EXISTS users")
    
    # Create new table structure with password fields
    sql = """ CREATE TABLE users ( 
    ID INTEGER PRIMARY KEY AUTOINCREMENT, 
    Username TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL,
    Password_hash TEXT NOT NULL) """ 
    
    # Execute the CREATE TABLE statement
    curr.execute(sql)
    
    # Save changes to database
    conn.commit()
    
    # Close the database connection
    conn.close()
    
   