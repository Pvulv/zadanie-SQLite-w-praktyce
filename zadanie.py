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

def select_all(conn, table):
   """
   Query all rows in the table
   :param conn:
   :return:
   """
   cur = conn.cursor()
   cur.execute(f"SELECT * FROM {table}")
   rows = cur.fetchall()

   print(rows)

def select_where(conn, table, **query):
   """
   Query tasks from table with data from **query dict
   :param conn:
   :param table:
   :param query:
   :return:
   """
   cur = conn.cursor()
   qs = []
   values = ()
   for k, v in query.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)
   cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
   rows = cur.fetchall()
   print(rows)

def archive_order(conn):
    """
    Archive orders with status 'zrealizowane' by moving them to archived_orders and deleting from orders.
    Show a message only if any orders were archived.
    :param conn:
    """
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders WHERE status = 'zrealizowane'")
        orders_to_archive = cur.fetchall()

        if not orders_to_archive:
            print("Brak zamówień do archiwizacji.")
            return

        sql_insert = '''INSERT INTO archived_orders(zamowienie_id, klient_id, data_zamowienia, kwota, status)
                        VALUES(?,?,?,?,?)'''
        for order in orders_to_archive:
            cur.execute(sql_insert, order)
        
        cur.execute("DELETE FROM orders WHERE status = 'zrealizowane'")
        
        conn.commit()
        print("Zamówienia zostały zarchiwizowane.")
    except Error as e:
        print(f"Błąd archiwizacji zamówień: {e}")

if __name__ == '__main__':

    create_clients_sql = """
    -- clients table
    CREATE TABLE IF NOT EXISTS clients (
        klient_id INTEGER PRIMARY KEY,
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
    create_archived_orders_sql = """
    -- archived_orders table
    CREATE TABLE IF NOT EXISTS archived_orders (
        zamowienie_id INTEGER PRIMARY KEY,
        klient_id INTEGER,
        data_zamowienia DATE,
        kwota DECIMAL(10,2),
        status TEXT NOT NULL,
        FOREIGN KEY (klient_id) REFERENCES clients(klient_id)
    );
    """

    file = "zadanie.db"
    conn = connection(file)

    if conn is not None:
        execute_sql(conn, create_clients_sql)
        execute_sql(conn, create_orders_sql)
        execute_sql(conn, create_archived_orders_sql)

    client_1 = ("Jan", "Kowalski", "jan.kowalski@email.com", "123-456-789",	"ul. Zielona 12, Warszawa",	"2023-01-15")
    client_2 = ("Anna", "Nowak", "anna.nowak@email.com", "987-654-321", "ul. Kwiatowa 45, Kraków", "2023-02-20")
    
    client_id_1 = add_client(conn, client_1)
    client_id_2 = add_client(conn, client_2)

    order_1 = (client_id_1, "2023-03-01", 250.50, "zrealizowane")
    order_2 = (client_id_2, "2023-04-10", 150.00, "w trakcie")
    
    add_order(conn, order_1)
    add_order(conn, order_2)
        
    update(conn, "orders", 2, status = "wysłane")

    select_all(conn, "clients")
    select_where(conn, "orders", status = "wysłane")

    archive_order(conn)

    conn.commit()
    conn.close()