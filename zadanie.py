import sqlite3
from sqlite3 import Error

def connection (file):
    """ create a datebase connection to a SQLite database 
        specifies by file
    :param file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(file)
        return conn
    except Error as e:
        print(e)
    return conn

def execute_sql(conn, sql):
   """ Execute sql
   :param conn: Connection object
   :param sql: a SQL script
   :return:
   """
   try:
       c = conn.cursor()
       c.execute(sql)
   except Error as e:
       print(e)
