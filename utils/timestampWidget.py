import sqlite3


def get_Timestamp(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT time FROM Date WHERE key='Zuletzt aktualisiert'")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None



def add_Timestamp(db_path, zeitstempel):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO Date (key, time) VALUES ('Zuletzt aktualisiert', ?)", (zeitstempel,))
    conn.commit()
    conn.close()
