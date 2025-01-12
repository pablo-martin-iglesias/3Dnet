import sqlite3

def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')

    # Tabla de solicitudes de printers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS printer_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            characteristics TEXT,
            materials TEXT,
            location TEXT,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Tabla de solicitudes de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS client_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            requirements TEXT,
            budget REAL,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Tabla de anuncios publicados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            printer_id INTEGER,
            description TEXT,
            materials TEXT,
            price_range TEXT,
            FOREIGN KEY(printer_id) REFERENCES printer_requests(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Base de datos creada con éxito.")

if __name__ == '__main__':
    create_tables()
