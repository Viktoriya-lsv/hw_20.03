import psycopg2

conn = psycopg2.connect(database ="net_db", user = "postgres", password = "vika7333")
def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS clients("
                    "id SERIAL PRIMARY KEY,"
                    "first_name VARCHAR(40) NOT NULL,"
                    "last_name VARCHAR(40) NOT NULL,"
                    "email VARCHAR(50) NOT NULL UNIQUE);")
        cur.execute("CREATE TABLE IF NOT EXISTS phones("
                    "id SERIAL PRIMARY KEY,"
                    "client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE,"
                    "phone VARCHAR(20) UNIQUE);")
    conn.commit()

def add_client(conn, first_name, last_name, email, phones = None):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO clients(first_name, last_name, email)"
                    "VALUES (%s, %s, %s) RETURNING id;"
                    "", (first_name, last_name, email))
        client_id = cur.fetchone()[0]
        if phones:
            for phone in phones:
                cur.execute("INSERT INTO phones (client_id, phone)"
                            "VALUES (%s, %s);"
                            "", (client_id, phone))
    conn.commit()
    return client_id

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO phones (client_id, phone)"
                    "VALUES (%s, %s);"
                    "", (client_id, phone))
    conn.commit()

def change_client(conn, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        if first_name:
            cur.execute("UPDATE clients SET first_name = %s WHERE id = %s;"
                        "",(first_name, client_id))
        if last_name:
            cur.execute("UPDATE clients SET last_name = %s WHERE id = %s;"
                        "", (last_name, client_id))
        if email:
            cur.execute("UPDATE clients SET email = %s WHERE id = %s;"
                        "", (email, client_id))
        if phones is not None:
            cur.execute("DELETE FROM phones WHERE client_id = %s;"
                        "", (client_id,))
            for phone in phones:
                cur.execute("INSERT INTO phones(client_id, phone)"
                            "VALUES (%s, %s);"
                            "", (client_id, phone))
    conn.commit()

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        for phone in phones:
            cur.execute("DELETE FROM phones WHERE client_id = %s AND phone = %s;"
                        "", (client_id, phone))
    conn.commit()

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM clients WHERE id = %s;"
                    "", (client_id,))
    conn.commit()

def find_client(conn, client_id = None, first_name = None, last_name = None, email = None,
                phone = None):
    with conn.cursor() as cur:
        if first_name:
            cur.execute("SELECT id FROM clients WHERE first_name = %s;"
                        "", (first_name,))
        if last_name:
            cur.execute("SELECT id FROM clients WHERE last_name = %s;"
                        "", (last_name,))
        if email:
            cur.execute("SELECT id FROM clients WHERE email = %s;"
                        "", (email,))
        if phone:
            cur.execute("SELECT client_id FROM phones WHERE phone = %s;"
                        "", (phone, ))
        return cur.fetchone()