
import sqlite3
import random
from Backend.dbPfad import db_pfad


def lottozahlen():
    
    bereits_gezogen = []

    try:
        with sqlite3.connect(db_pfad()) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                           SELECT "Hauptzahl 1", "Hauptzahl 2", "Hauptzahl 3", "Hauptzahl 4", "Hauptzahl 5", "Zusatzzahl 1", "Zusatzzahl 2"
                           FROM Eurojackpot
                           """)
            for zeile in cursor.fetchall():
                hauptzahlen = tuple(sorted(map(int, zeile[:5])))
                zusatzzahlen = tuple(sorted(map(int, zeile[5:])))
                bereits_gezogen.append((hauptzahlen, zusatzzahlen))
    except sqlite3.Error as e:
        return f"❌ Datenbankfehler: {e}"

    for _ in range(1000):
        wahl1 = tuple(sorted(random.sample([zahl for zahl in range(1,51)], k=5)))
        wahl2 = tuple(sorted(random.sample([zahl for zahl in range(1,13)], k=2)))
        gezogen = wahl1, wahl2
        if gezogen in bereits_gezogen:
            continue
        hauptzahlen = " - ".join(map(str, gezogen[0]))
        zusatzzahlen = " - ".join(map(str, gezogen[1]))
        return (f"{hauptzahlen}        {zusatzzahlen}")
    
    return "⚠️ Alle Zahlenkombinationen, die es gibt, wurden bereits gezogen!"

