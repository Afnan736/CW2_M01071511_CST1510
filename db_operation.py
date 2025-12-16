import sqlite3
import pandas as pd 

def db_md():

   # Import datasets metadata from CSV and store in SQLite database. Reads the 'datasets_metadata.csv' file and saves it as a table in the database.
    
    # Read metadata from CSV file
    metadata = pd.read_csv('DATA/datasets_metadata.csv')
    
    # Connect to SQLite database
    conn = sqlite3.connect('DATA/intelligence_platform.db') 
    
    # Save metadata to SQL table, replace if exists
    metadata.to_sql('datasets_metadata', conn, if_exists='replace', index=False)
    print('Migrated all datasets_metadata')
    
    # Close database connection
    conn.close()  

def it_ticket():

   #  Import IT tickets data from CSV and store in SQLite database. Reads the 'it_tickets.csv' file and saves it as a table in the database.
   
    # Read IT tickets from CSV file
    it_tickets = pd.read_csv('DATA/it_tickets.csv')
    
    # Connect to SQLite database
    conn = sqlite3.connect('DATA/intelligence_platform.db') 
    
    # Save IT tickets to SQL table, replace if exists
    it_tickets.to_sql('it_tickets', conn, if_exists='replace', index=False)
    print('Migrated all it_tickets')
    
    # Close database connection
    conn.close()

def get_cyber_incidents():
    """
    Fetch cyber incidents data from SQLite database.
    Returns all records from the 'cyber_incidents' table as a pandas DataFrame.
    """
    # Connect to SQLite database
    conn = sqlite3.connect('DATA/intelligence_platform.db')
    
    # SQL query to get all cyber incidents
    sql = 'SELECT * FROM cyber_incidents'
    
    # Execute query and load results into DataFrame
    data = pd.read_sql(sql, conn)
    
    # Close database connection
    conn.close()
    
    return data
 
def database():
    """
    Main database setup function.
    Runs all migration functions to populate the database with data.
    """
    print("Setting up database...")  
    
    # Migrate metadata table
    db_md()
    
    # Migrate IT tickets table
    it_ticket()
    
    print("Database complete!")

# Entry point: run database setup when script is executed directly
if __name__ == "__main__":
    database()