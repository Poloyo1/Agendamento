from src.database.db import get_connection

def get_session(phone):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT step, service, date, time FROM sessions WHERE phone = ?", (phone,))
    row = cursor.fetchone()

    if not row:
        cursor.execute(
            "INSERT INTO sessions (phone, step) VALUES (?, ?)",
            (phone, 1)
        )
        conn.commit()
        conn.close()
        return {"step": 1}

    conn.close()
    return {
        "step": row[0],
        "service": row[1],
        "date": row[2],
        "time": row[3]
    }

def update_session(phone, data):
    conn = get_connection()
    cursor = conn.cursor()

    for key, value in data.items():
        cursor.execute(
            f"UPDATE sessions SET {key} = ? WHERE phone = ?",
            (value, phone)
        )

    conn.commit()
    conn.close()

def clear_session(phone):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM sessions WHERE phone = ?", (phone,))
    conn.commit()
    conn.close()
