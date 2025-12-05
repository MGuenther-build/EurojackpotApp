
import sqlite3
import re
from backend.dbPath import db_pfad


def zahlen_eintragen(eintrag):
    
    if isinstance(eintrag, str):
        eintrag = re.split(r"[,\s;]+", eintrag.strip())

    try:
        zahlen = [int(z) for z in eintrag]
    except ValueError:
        return "⚠️ Ungültige Eingabe! Bitte nur Zahlen eingeben!"
    if len(zahlen) != 7:
        return "⚠️ Ungültige Eingabe! Es müsssen 7 Zahlen sein!"
    
    hauptzahlen = sorted(zahlen[:5])
    zusatzzahlen = sorted(zahlen[5:])
    zahlen = hauptzahlen + zusatzzahlen

    if not all(1 <= z <= 50 for z in hauptzahlen):
        return "⚠️ Fehler! Eine oder mehrere Hauptzahlen liegen außerhalb des Ziehungsbereichs."
    if not all(1 <= z <= 12 for z in zusatzzahlen):
        return "⚠️ Fehler! Eine oder mehrere Zusatzzahlen liegen außerhalb des Ziehungsbereichs."
    if ((len(set(hauptzahlen)) != (len(hauptzahlen)) and (len(set(zusatzzahlen))) != len(zusatzzahlen))):
        return "⚠️ Mindestens eine Hauptzahl und die Zusatzzahlen sind doppelt!"
    elif len(set(hauptzahlen)) != len(hauptzahlen):
        return "⚠️ Mindestens eine Hauptzahl ist doppelt!"
    elif len(set(zusatzzahlen)) != len(zusatzzahlen):
        return "⚠️ Die Zusatzzahlen sind doppelt!"
    
    try:
        with sqlite3.connect(db_pfad()) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                        SELECT COUNT(*) FROM Eurojackpot
                        WHERE    "Hauptzahl 1" = ? AND
                                    "Hauptzahl 2" = ? AND
                                    "Hauptzahl 3" = ? AND
                                    "Hauptzahl 4" = ? AND
                                    "Hauptzahl 5" = ? AND
                                    "Zusatzzahl 1" = ? AND
                                    "Zusatzzahl 2" = ?
                        """, tuple(zahlen))
            
            if cursor.fetchone()[0] > 0:
                return "⚠️ Lottozahlen bereits vorhanden!"
    
    
            cursor.execute("""
                    INSERT INTO Eurojackpot ("Hauptzahl 1", "Hauptzahl 2", "Hauptzahl 3", "Hauptzahl 4", "Hauptzahl 5", "Zusatzzahl 1", "Zusatzzahl 2")
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, tuple(zahlen))
            connection.commit()
            return "✅ Lottozahlen hinzugefügt"
    
    except sqlite3.Error as e:
        return f"❌ Fehler beim Zahlen eintragen: {e}"
