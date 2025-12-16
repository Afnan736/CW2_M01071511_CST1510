import pandas as pd

# Load cyber incidents from CSV to database
def migrate_cyber_incidents(conn): 
    cyber = pd.read_csv('DATA/cyber_incidents.csv') 
    cyber.to_sql('cyber_incidents', conn, if_exists='replace', index=False) 
    print('Migrated cyber incidents') 
    conn.close()

# Get all cyber incidents from database
def get_cyber_incidents(conn): 
    sql = 'SELECT * FROM cyber_incidents' 
    data = pd.read_sql(sql, conn)
    conn.close() 
    return data

# Add new incident
def add_incident(conn, incident_id, timestamp, severity, category, status, description):
    try: 
        curr = conn.cursor() 
        curr.execute("""
            INSERT INTO cyber_incidents 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (incident_id, timestamp, severity, category, status, description)) 
        conn.commit()
        return True 
    except Exception as e: 
        print(f"Error adding incident: {e}") 
        return False

# Update incident
def update_incident(conn, incident_id, severity, category, status, description): 
    try: 
        curr = conn.cursor() 
        curr.execute("""
            UPDATE cyber_incidents 
            SET severity=?, category=?, status=?, description=? 
            WHERE incident_id=?
        """, (severity, category, status, description, incident_id)) 
        conn.commit()
        return True 
    except Exception as e: 
        print(f"Error updating incident: {e}") 
        return False

# Delete incident
def delete_incident(conn, incident_id): 
    try: 
        curr = conn.cursor() 
        curr.execute("DELETE FROM cyber_incidents WHERE incident_id=?", (incident_id,)) 
        conn.commit() 
        return True 
    except Exception as e:
        print(f"Error deleting incident: {e}") 
        return False