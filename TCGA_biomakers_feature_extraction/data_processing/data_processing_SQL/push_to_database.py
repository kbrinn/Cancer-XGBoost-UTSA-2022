import os
import sqlite3

'''
script to push data into DB. For time contrainst, the script has to be run locally on each TCGA folder.
'''

def createTable(cursor):
   try:
      query1 = """ CREATE TABLE IF NOT EXISTS Person (
               id integer PRIMARY KEY,
               person text NOT NULL UNIQUE,
               cancerType text NOT NULL   
            );"""
      cursor.execute(query1)

      query2 = """ CREATE TABLE Data (
               id INTEGER,
            geneType	TEXT,
            count	REAL,
            person_id	INTEGER,
            FOREIGN KEY(person_id) REFERENCES Person(id),
            PRIMARY KEY(id)
            );"""
      cursor.execute(query2)
   except:
      print("Database already Exists")

def push_data(conn, cursor, title, content, cancerType):
   try:
      query = ''' INSERT INTO Person(person, cancerType)
                 VALUES(? ,?) '''
      cursor.execute(query, [title, cancerType])
      conn.commit()

      query = ''' SELECT id FROM Person where person = ? '''
      print(title)
      cursor.execute(query,[title])
      id = cursor.fetchall()[0][0]
      print(id)

      query = ''' INSERT INTO Data(geneType, count,person_id )
                    VALUES(?,?,?) '''
      newcontent = [(x[0],float(x[1][0]),id) for x in content[:-1]]

      cursor.executemany(query,newcontent)
      cursor.execute(query,[content[-1][0],content[-1][1],id])
      conn.commit()
   except:
      print("Same Data entered Skipping...")

def enterDatabase(fileName, cancerType):
   with open(fileName, 'r') as file:
      values = file.read().split('\n')

   title = eval(values[1].split(": {")[0])
   content = [[eval(y) for y in x.split(':')] for x in values[2:-2]]

   conn = sqlite3.connect("Cancer.db", isolation_level='DEFERRED')
   cursor = conn.cursor()
   createTable(cursor)
   content[-1] = [content[-1][0], (content[-1][1])]
   push_data(conn, cursor, title, content, cancerType)


cancerType = 'TGCT'

path = os.curdir
for dirpath, _, filenames in os.walk(path):
   for f in filenames:
      if '.json' in f:
         print(os.path.abspath(os.path.join(dirpath, f)))
         enterDatabase(os.path.abspath(os.path.join(dirpath, f)), cancerType)

