import pandas as pd


# Load datasets metadata from CSV to database
def db_md(conn):
    metadata = pd.read_csv('DATA/datasets_metadata.csv') 
    metadata.to_sql('datasets_metadata', conn, if_exists='replace', index=False)
    print('Migrated all datasets_metadata')
    conn.close()


# Get all datasets metadata from database
def get_db_md(conn):
    sql = 'SELECT * FROM datasets_metadata'
    data = pd.read_sql(sql, conn)
    conn.close()
    return data


# Add new dataset to database
def add_md(conn, dataset_id, name, rows, columns, uploaded_by, upload_date):
    try:
        curr = conn.cursor()
        curr.execute("""
            INSERT INTO datasets_metadata (dataset_id, name, rows, columns, uploaded_by, upload_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (dataset_id, name, rows, columns, uploaded_by, upload_date))
        conn.commit()
        return True
    except Exception as e:
        print(f"Add error: {e}")
        return False


# Update existing dataset
def update_md(conn, dataset_id, name, rows, columns, uploaded_by, upload_date):
    try:
        curr = conn.cursor()
        curr.execute("""
            UPDATE datasets_metadata
            SET name = ?, rows = ?, columns = ?, uploaded_by = ?, upload_date = ?
            WHERE dataset_id = ?
        """, (name, rows, columns, uploaded_by, upload_date, dataset_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Update error: {e}")
        return False


# Delete dataset from database
def delete_md(conn, dataset_id):
    try:
        curr = conn.cursor()
        curr.execute("DELETE FROM datasets_metadata WHERE dataset_id = ?", (dataset_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Delete error: {e}")
        return False