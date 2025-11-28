def cte_user_table():
    conn = sqlite3.connect('DATA/intelligence_platform.db')  
    curr = conn.cursor()
    # First drop the existing table
    curr.execute("DROP TABLE IF EXISTS users")
    # Then create new table structure with password
    sql = """ CREATE TABLE users ( 
    ID INTEGER PRIMARY KEY AUTOINCREMENT, 
    Username TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL,
    Password_hash TEXT NOT NULL) """ 
    curr.execute(sql)
    conn.commit()
    conn.close()
    print("Users table recreated with new structure")