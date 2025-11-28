def migrate_cyber_incidents():
    cyber = pd.read_csv('DATA/cyber_incidents.csv')
    conn = sqlite3.connect('DATA/intelligence_platform.db') 
    cyber.to_sql('cyber_incidents', conn, if_exists='replace', index=False)
    print('Migrated all cyber_incidents')
    conn.close()

    
def get_cyber_incidents():
 sql = 'SELECT * FROM cyber_incidents'
 data = pd.read_sql(sql,conn)
 conn.close()
 return data