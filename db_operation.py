import sqlite3
import pandas as pd 

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

def cte_cyber_incidents_table():
    conn = sqlite3.connect('DATA/intelligence_platform.db')  
    curr = conn.cursor()
    # Drop existing cyber_incidents table
    curr.execute("DROP TABLE IF EXISTS cyber_incidents")
    conn.commit()
    conn.close()
    print("Cyber incidents table ready for migration")

def add_user(conn, username, password, hash_password):  
    curr = conn.cursor()
    sql = """ INSERT INTO users (Username, Password, Password_hash) VALUES (?, ?, ?) """  
    para = (username, password, hash_password)  
    curr.execute(sql, para)
    conn.commit()

def migrate_users():
    conn = sqlite3.connect('DATA/intelligence_platform.db') 
    with open('DATA/user.txt') as f:
        users = f.readlines()

    for user in users:
        fname, lname, password, hash_val = user.strip().split(',')
        username = fname + lname
        add_user(conn, username, password, hash_val)  
    conn.close()  
    print("Users migrated successfully")

def get_all_users():
    conn = sqlite3.connect('DATA/intelligence_platform.db')  
    curr = conn.cursor()
    sql = "SELECT * FROM users"
    curr.execute(sql)
    users = curr.fetchall()
    conn.close()
    return users

def migrate_cyber_incidents():
    cyber = pd.read_csv('DATA/cyber_incidents.csv')
    conn = sqlite3.connect('DATA/intelligence_platform.db') 
    cyber.to_sql('cyber_incidents', conn, if_exists='replace', index=False)
    print('Migrated all cyber_incidents')
    conn.close()

def db_md():
        metadata =pd.read_csv('DATA/datasets_metadata.csv')
        conn = sqlite3.connect('DATA/intelligence_platform.db') 
        metadata.to_sql('datasets_metadata', conn, if_exists='replace', index=False)
        print('Migrated all datasets_metadata')
        conn.close()  

def it_ticket():
    it_tickets = pd.read_csv('DATA/it_tickets.csv')
    conn = sqlite3.connect('DATA/intelligence_platform.db') 
    it_tickets.to_sql('it_tickets', conn, if_exists='replace', index=False)
    print('Migrated all it_tickets')
    conn.close()


def get_cyber_incidents():
 sql = 'SELECT * FROM cyber_incidents'
 data = pd.read_sql(sql,conn)
 conn.close()
 return data
 
conn = sqlite3.connect('DATA/intelligence_platform.db') #
print(get_cyber_incidents())

"""def read_all_cyber_incidents_pandas():  
    conn = sqlite3.connect('DATA/intelligence_platform.db') 
    query = "SELECT * FROM cyber_incidents"
    cyber_table = pd.read_sql(query, conn)
    conn.close()  
    print(cyber_table.head(5))
    return cyber_table"""

# Run all functions to set up both tables
"""def database():
    print("Setting up database...")
    cte_user_table()           
    cte_cyber_incidents_table() 
    migrate_users()            
    migrate_cyber_incidents()  
    print("Database setup complete!")
    
    print("\nSample user data:")
    users = get_all_users()
    for user in users:
        print(user)
        
    print("\nSample cyber incidents data:")
    read_all_cyber_incidents_pandas()"""


