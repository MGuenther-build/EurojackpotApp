
import sqlite3
import re
from backend.dbPath import db_pfad


def check_zahlen(mein_tipp):
    
    try:
        mein_tipp = list(map(int, re.split(r"[,\s;]+", mein_tipp)))
        if len(mein_tipp) <7:
            return "⚠️ Zu wenige Zahlen! Es müssen 5 Hauptzahlen und 2 Zusatzzahlen sein."
        elif len(mein_tipp) >7:
            return "⚠️ Zu viele Zahlen! Es müssen 5 Hauptzahlen und 2 Zusatzzahlen sein."
        elif mein_tipp == [1,2,3,4,5,6,7]:
            return "🚨 Nicht Dein Ernst?! Selbst wenn sie gezogen werden sollten, haben diese Zahlen garantiert Tausende Spaßtipper auch!"
        hauptzahlen = mein_tipp[:5]
        zusatzzahlen = mein_tipp[5:]
        if not all(1 <= zahl <= 50 for zahl in hauptzahlen) and not all(1 <= zahl <= 12 for zahl in zusatzzahlen) and (len(set(hauptzahlen)) and len(set(zusatzzahlen))) != (len(hauptzahlen) and len(zusatzzahlen)):
            return "⚠️ Alles falsch gemacht! Haupt- und Zusatzzahlen doppelt und außerhalb des Ziehungsbereichs!"      
        if not all(1 <= zahl <= 50 for zahl in hauptzahlen) and len(set(hauptzahlen)) != len(hauptzahlen):
            return "⚠️ Ungültige Hauptzahlen! Eine oder mehrere Hauptzahlen wurden doppelt getippt und liegen außerhalb des Ziehungsbereichs!"
        if not all(1 <= zahl <= 12 for zahl in zusatzzahlen) and len(set(zusatzzahlen)) != len(zusatzzahlen):
            return "⚠️ Ungültige Zusatzzahlen! Die Zusatzzahlen wurden doppelt getippt und liegen zudem außerhalb des Ziehungsbereichs!"    
        if ((len(set(hauptzahlen)) != (len(hauptzahlen)) and (len(set(zusatzzahlen))) != len(zusatzzahlen))):
            return "⚠️ Mindestens eine Hauptzahl und die Zusatzzahlen wurden doppelt getippt!"
        elif len(set(hauptzahlen)) != len(hauptzahlen):
            return "⚠️ Mindestens eine Hauptzahl wurde doppelt getippt!"
        elif len(set(zusatzzahlen)) != len(zusatzzahlen):
            return "⚠️ Die Zusatzzahlen wurden doppelt getippt!"
        if not all(1 <= zahl <= 50 for zahl in hauptzahlen) and not all(1 <= zahl <= 12 for zahl in zusatzzahlen):
            return "⚠️ Ungültige Zahlen! Eine oder mehere Hauptzahlen als auch Zusatzzahlen liegen nicht im Ziehungsbereich!"
        if not all(1 <= zahl <= 50 for zahl in hauptzahlen):
            return "⚠️ Ungültige Hauptzahlen! Eine oder mehrere Hauptzahlen liegen nicht im Ziehungsbereich von 1 bis 50!"
        if not all(1 <= zahl <= 12 for zahl in zusatzzahlen):
            return "⚠️ Ungültige Zusatzzahlen! Eine oder beide Zusatzzahlen liegen nicht im Ziehungsbereich von 1 bis 12!"
    except ValueError:
        return "❌ Fehler in der Eingabe! Es wurden keine gültigen Zahlen eingegeben."
            
    try:
        with sqlite3.connect(db_pfad()) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                           SELECT "Hauptzahl 1", "Hauptzahl 2", "Hauptzahl 3", "Hauptzahl 4", "Hauptzahl 5", "Zusatzzahl 1", "Zusatzzahl 2"
                           FROM Eurojackpot
                           """)
            total = cursor.fetchall()

            for zeile in total:
                hauptzahlen = sorted(zeile[:5])
                zusatzzahlen = sorted(zeile[5:])
                if sorted(mein_tipp[:5]) == sorted(hauptzahlen) and sorted(mein_tipp[5:]) == sorted(zusatzzahlen):
                    return "❌ Wurden bereits gezogen!"
    except sqlite3.Error as e:
        return str(e)
    return "✅ Diese Zahlen sind ok!"
