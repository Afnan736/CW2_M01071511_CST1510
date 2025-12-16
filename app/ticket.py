import pandas as pd


# Load IT tickets data from CSV to database
def migrate_it_tickets(conn):
    it_tickets = pd.read_csv('DATA/it_tickets.csv')
    it_tickets.to_sql('it_ticket', conn, if_exists='replace', index=False)
    print('Migrated all it_tickets')
    conn.close()


# Get all IT tickets from database
def get_it_tickets(conn):
    sql = 'SELECT * FROM it_tickets'
    data = pd.read_sql(sql, conn)
    conn.close()
    return data


# Add new IT ticket to database
def add_ticket(conn, ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours):
    try:
        curr = conn.cursor()
        curr.execute("""
            INSERT INTO it_ticket (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours))
        conn.commit()
        return True
    except Exception as e:
        print(f"Add error: {e}")
        return False


# Update existing IT ticket
def update_ticket(conn, ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours):
    try:
        curr = conn.cursor()
        curr.execute("""
            UPDATE it_ticket
            SET priority = ?, description = ?, status = ?, assigned_to = ?, created_at = ?, resolution_time_hours = ?
            WHERE ticket_id = ?
        """, (priority, description, status, assigned_to, created_at, resolution_time_hours, ticket_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Update error: {e}")
        return False


# Delete IT ticket from database
def delete_ticket(conn, ticket_id):
    try:
        curr = conn.cursor()
        curr.execute("DELETE FROM it_ticket WHERE ticket_id = ?", (ticket_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Delete error: {e}")
        return False