import pandas as pd

def db_md(conn):
        metadata =pd.read_csv('DATA/datasets_metadata.csv') 
        metadata.to_sql('datasets_metadata', conn, if_exists='replace', index=False)
        print('Migrated all datasets_metadata')
        conn.close()


def get_db_md(conn):
 sql = 'SELECT * FROM datasets_metadata'
 data = pd.read_sql(sql,conn)
 conn.close()
 return data