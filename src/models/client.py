from src.database.db import get_connection

def get_client_by_phone(phone):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, calendar_id, active FROM clients WHERE phone = ?",
        (phone,)
    )

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "name": row[1],
            "calendar_id": row[2],
            "active": row[3]
        }
    return None
def create_client(name, phone, calendar_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO clients (name, phone, calendar_id)
        VALUES (?, ?, ?)
    """, (name, phone, calendar_id))

    conn.commit()
    conn.close()
