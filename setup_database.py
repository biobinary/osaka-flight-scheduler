import sqlite3

def init_db():
    conn = sqlite3.connect('flights.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            departure_time TEXT,
            destination TEXT,
            airline TEXT,
            flight_code TEXT,
            gate TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()
