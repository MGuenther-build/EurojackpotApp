import sqlite3
import re
from backend.dbPath import db_path


def add_draw(record):
    
    if isinstance(record, str):
        record = re.split(r"[,\s;]+", record.strip())

    try:
        nums = [int(z) for z in record]
    except ValueError:
        return "⚠️ Ungültige Eingabe! Bitte nur Zahlen eingeben!"
    if len(nums) != 7:
        return "⚠️ Ungültige Eingabe! Es müsssen 7 Zahlen sein!"
    
    main_numbers = sorted(nums[:5])
    additional_numbers = sorted(nums[5:])
    nums = main_numbers + additional_numbers

    if not all(1 <= z <= 50 for z in main_numbers):
        return "⚠️ Fehler! Eine oder mehrere Hauptzahlen liegen außerhalb des Ziehungsbereichs."
    if not all(1 <= z <= 12 for z in additional_numbers):
        return "⚠️ Fehler! Eine oder mehrere Zusatzzahlen liegen außerhalb des Ziehungsbereichs."
    if ((len(set(main_numbers)) != (len(main_numbers)) and (len(set(additional_numbers))) != len(additional_numbers))):
        return "⚠️ Mindestens eine Hauptzahl und die Zusatzzahlen sind doppelt!"
    elif len(set(main_numbers)) != len(main_numbers):
        return "⚠️ Mindestens eine Hauptzahl ist doppelt!"
    elif len(set(additional_numbers)) != len(additional_numbers):
        return "⚠️ Die Zusatzzahlen sind doppelt!"
    
    try:
        with sqlite3.connect(db_path()) as connection:
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
                        """, tuple(nums))
            
            if cursor.fetchone()[0] > 0:
                return "⚠️ Lottozahlen bereits vorhanden!"
    
    
            cursor.execute("""
                    INSERT INTO Eurojackpot ("Hauptzahl 1", "Hauptzahl 2", "Hauptzahl 3", "Hauptzahl 4", "Hauptzahl 5", "Zusatzzahl 1", "Zusatzzahl 2")
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, tuple(nums))
            connection.commit()
            return "✅ Lottozahlen hinzugefügt"
    
    except sqlite3.Error as e:
        return str(e)
