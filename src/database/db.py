import sqlite3

DB_NAME = "saas.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def get_client_by_phone(phone):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, calendar_id FROM clients WHERE phone = ?",
        (phone,)
    )

    client = cursor.fetchone()
    conn.close()
    return client



def init_db():
    conn = get_connection()
    cursor = conn.cursor()



    # CLIENTES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT UNIQUE,
            calendar_id TEXT,
            active INTEGER DEFAULT 1
        )
    """)

    # SESSÕES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            phone TEXT PRIMARY KEY,
            step INTEGER,
            service TEXT,
            date TEXT,
            time TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    phone TEXT,
    service TEXT,
    date TEXT,
    time TEXT,
    google_event_id TEXT,
    google_event_link TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id)
)
    """)

    conn.commit()
    conn.close()


def save_appointment(client_id, phone, service, date, time, event):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO appointments
        (client_id, phone, service, date, time, google_event_id, google_event_link)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        client_id,
        phone,
        service,
        date,
        time,
        event["id"],
        event["htmlLink"]
    ))