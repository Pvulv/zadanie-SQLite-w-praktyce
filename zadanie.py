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

def add_client(conn, client):
    """
    Create a new client into the clients table
    :param conn:
    :param client:
    :return: client id
    """
    sql = '''INSERT INTO clients(imie, nazwisko, email, numer_tel, adres, data)
                VALUES(?,?,?,?,?,?)
                ON CONFLICT(numer_tel) DO NOTHING;'''
    cur = conn.cursor()
    cur.execute(sql, client)
    return cur.lastrowid

if __name__ == '__main__':

    create_clients_sql = """
    -- clients table
    CREATE TABLE IF NOT EXISTS clients (
        klient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        imie TEXT NOT NULL,
        nazwisko TEXT NOT NULL,
        email TEXT,
        numer_tel VARCHAR(15) UNIQUE,
        adres VARCHAR(150),
        data DATE
    );
    """