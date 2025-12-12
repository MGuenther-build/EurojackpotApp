import sqlite3
import re
from backend.dbPath import db_path


def check_picks(my_bet):
    try:
        my_bet = list(map(int, re.split(r"[,\s;]+", my_bet)))
        if len(my_bet) <7:
            return "⚠️ Zu wenige Zahlen! Es müssen 5 Hauptzahlen und 2 Zusatzzahlen sein."
        elif len(my_bet) >7:
            return "⚠️ Zu viele Zahlen! Es müssen 5 Hauptzahlen und 2 Zusatzzahlen sein."
        elif my_bet == [1,2,3,4,5,6,7]:
            return "🚨 Nicht Dein Ernst?! Selbst wenn sie gezogen werden sollten, haben diese Zahlen garantiert Tausende Spaßtipper auch!"
        main_numbers = my_bet[:5]
        additional_numbers = my_bet[5:]
        if not all(1 <= num <= 50 for num in main_numbers) and not all(1 <= num <= 12 for num in additional_numbers) and (len(set(main_numbers)) and len(set(additional_numbers))) != (len(main_numbers) and len(additional_numbers)):
            return "⚠️ Alles falsch gemacht! Haupt- und Zusatzzahlen doppelt und außerhalb des Ziehungsbereichs!"      
        if not all(1 <= num <= 50 for num in main_numbers) and len(set(main_numbers)) != len(main_numbers):
            return "⚠️ Ungültige Hauptzahlen! Eine oder mehrere Hauptzahlen wurden doppelt getippt und liegen außerhalb des Ziehungsbereichs!"
        if not all(1 <= num <= 12 for num in additional_numbers) and len(set(additional_numbers)) != len(additional_numbers):
            return "⚠️ Ungültige Zusatzzahlen! Die Zusatzzahlen wurden doppelt getippt und liegen zudem außerhalb des Ziehungsbereichs!"    
        if ((len(set(main_numbers)) != (len(main_numbers)) and (len(set(additional_numbers))) != len(additional_numbers))):
            return "⚠️ Mindestens eine Hauptzahl und die Zusatzzahlen wurden doppelt getippt!"
        elif len(set(main_numbers)) != len(main_numbers):
            return "⚠️ Mindestens eine Hauptzahl wurde doppelt getippt!"
        elif len(set(additional_numbers)) != len(additional_numbers):
            return "⚠️ Die Zusatzzahlen wurden doppelt getippt!"
        if not all(1 <= num <= 50 for num in main_numbers) and not all(1 <= num <= 12 for zahl in additional_numbers):
            return "⚠️ Ungültige Zahlen! Eine oder mehere Hauptzahlen als auch Zusatzzahlen liegen nicht im Ziehungsbereich!"
        if not all(1 <= num <= 50 for num in main_numbers):
            return "⚠️ Ungültige Hauptzahlen! Eine oder mehrere Hauptzahlen liegen nicht im Ziehungsbereich von 1 bis 50!"
        if not all(1 <= num <= 12 for num in additional_numbers):
            return "⚠️ Ungültige Zusatzzahlen! Eine oder beide Zusatzzahlen liegen nicht im Ziehungsbereich von 1 bis 12!"
    except ValueError:
        return "❌ Fehler in der Eingabe! Es wurden keine gültigen Zahlen eingegeben."
            
    try:
        with sqlite3.connect(db_path()) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                           SELECT "Hauptzahl 1", "Hauptzahl 2", "Hauptzahl 3", "Hauptzahl 4", "Hauptzahl 5", "Zusatzzahl 1", "Zusatzzahl 2"
                           FROM Eurojackpot
                           """)
            total = cursor.fetchall()

            for row in total:
                main_numbers = sorted(row[:5])
                additional_numbers = sorted(row[5:])
                if sorted(my_bet[:5]) == sorted(main_numbers) and sorted(my_bet[5:]) == sorted(additional_numbers):
                    return "❌ Wurden bereits gezogen!"
    except sqlite3.Error as e:
        return str(e)
    return "✅ Diese Zahlen sind ok!"
