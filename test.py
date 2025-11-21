import sqlite3
import pandas as pd 

def cte_user_table():
    curr =conn.cursor()
    sql = """ CREATE TABLE IF NOT EXISTS users ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT NOT NULL UNIQUE, 
    password_hash TEXT NOT NULL) """ 
    curr.execute(sql)
    conn.commit()


def add_user(conn,name, hash_password):
  curr =conn.cursor()
  sql = """ INSERT INTO users (username, password_hash) VALUES (?, ?) """ 
  para =(name, hash_password)
  curr.execute(sql,para)
  conn.commit()

def migrate_users():
 with open('DATA/user.txt') as f:
   users = f.readlines()

 for user in users :
   name, hash = user.strip().split(',')
   add_user(conn, name, hash)
   
'''
conn = sqlite3.connect('DATA/intelligence_platform.db')
# add_user(conn,'rober','qwertyuiosdfg987654rfvy7890okmnbv')
#conn.close()
'''

def get_all_users():
   curr = conn.cursor()
   sql = "select * FROM users"
   curr.execute(sql)
   users = curr.fetchall()
   conn.close()
   return users

#print(get_all_users())


#conn = sqlite3.connect('DATA/intelligence_platform.db')  

def migrate_cyber_incidents():
   cyber = pd.read_csv('DATA/cyber_incidents.csv')
   #print(cyber.head(5))
   conn = sqlite3.connect('DATA/intelligence_platform.db') 
   cyber.to_sql('cyber_incidents',conn, if_exists='append',index=False)
   print('Migrated all cyber_incidents')


def real_all_cyber_incidents_pandas():
  conn = sqlite3.connect('DATA/intelligence_platform.db') 
  query = "select * FROM cyber_incidents"
  cyber_table = pd.read_sql(query,conn)
  print(cyber_table.head(5))
