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

def add_order(conn, order):
    """
    Create a new order into the orders table
    :param conn:
    :param order:
    :return: order id
    """
    klient_id = order[0]

    if klient_id == 0:
        print("Nie można dodać zamówienia dla klienta o ID 0.")
        return None 
    
    sql = '''INSERT INTO orders(klient_id, data_zamowienia, kwota, status)
            VALUES(?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, order)
    return cur.lastrowid

def update(conn, table, id, **kwargs):
    """
    update kwote, status of a order
    :param conn:
    :param table: table name
    :param id: row id 
    :return:
    """

    parametres = [f"{k} = ?" for k in kwargs]
    parametres = ", ".join(parametres)
    values = tuple(v for v in kwargs.values()) + (id, )

    id_column = "zamowienie_id" if table == "orders" else "klient_id"

    sql = f''' UPDATE {table}
                SET {parametres}
                WHERE {id_column} = ?'''
    
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print(f'Udało się zmienić dane w tabeli {table}, id: {id}')
    except sqlite3.OperationalError as e:
        print(e)

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
    create_orders_sql = """
    -- orders table
    CREATE TABLE IF NOT EXISTS orders (
        zamowienie_id INTEGER PRIMARY KEY,
        klient_id INTEGER,
        data_zamowienia DATE,
        kwota DECIMAL(10,2),
        status TEXT NOT NULL,
        FOREIGN KEY (klient_id) REFERENCES clients(klient_id)
        CONSTRAINT unique_order UNIQUE(klient_id, data_zamowienia)
    );
    """