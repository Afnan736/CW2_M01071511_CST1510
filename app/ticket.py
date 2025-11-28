


def it_ticket(conn):
    it_tickets = pd.read_csv('DATA/it_tickets.csv') 
    it_tickets.to_sql('it_tickets', conn, if_exists='replace', index=False)
    print('Migrated all it_tickets')
    conn.close()


def get_it_ticket():
 sql = 'SELECT * FROM it_ticket'
 data = pd.read_sql(sql,conn)
 conn.close()
 return data