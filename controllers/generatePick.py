import sqlite3
import random
from backend.dbPath import db_path


def generate_a_pick():
    
    already_drawn = []

    try:
        with sqlite3.connect(db_path()) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                           SELECT "Hauptzahl 1", "Hauptzahl 2", "Hauptzahl 3", "Hauptzahl 4", "Hauptzahl 5", "Zusatzzahl 1", "Zusatzzahl 2"
                           FROM Eurojackpot
                           """)
            for row in cursor.fetchall():
                main_numbers = tuple(sorted(map(int, row[:5])))
                additional_numbers = tuple(sorted(map(int, row[5:])))
                already_drawn.append((main_numbers, additional_numbers))
    except sqlite3.Error as e:
        return str(e)
    
    attempt = 0
    max_attempt = 140000000
    while attempt < max_attempt:
        attempt += 1
        choice1 = tuple(sorted(random.sample([pick for pick in range(1,51)], k=5)))
        choice2 = tuple(sorted(random.sample([pick for pick in range(1,13)], k=2)))
        drawn = choice1, choice2
        
        if drawn not in already_drawn:
            main_numbers = " - ".join(map(str, drawn[0]))
            additional_numbers = " - ".join(map(str, drawn[1]))
            return f"{main_numbers}        {additional_numbers}"
    
    return "⚠️ Alle möglichen Zahlenkombinationen wurden bereits gezogen!"
