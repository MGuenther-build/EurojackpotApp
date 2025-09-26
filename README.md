# EurojackpotApp

**EurojackpotApp** ist eine Python-basierte Anwendung, die es Dir ermöglicht gezogenen Eurojackpot-Zahlen zu verwalten, Deine Tipps zu vergleichen und neue Glückszahlen zu generieren. Die App nutzt Qt für die grafische Benutzeroberfläche und SQLite für die Speicherung der gezogenen Zahlen.

## Features

- **Datenbank der gezogenen Zahlen**: Alle jemals gezogenen Eurojackpot-Zahlen werden in einer SQLite-Datenbank gespeichert.
- **Vergleich deiner Tipps**: Du kannst deine eigenen Tipps mit den bereits gezogenen Zahlen vergleichen. Eine Benachrichtigung wird angezeigt, wenn dein Tipp bereits gezogen wurde.
- **Fehlerüberprüfung**: Deine Tipps werden auf Fehler überprüft, z.B. ob die Zahlen im gültigen Bereich liegen und ob es doppelte Zahlen gibt. Es wird zwischen Hauptzahlen und Zusatzzahlen unterschieden.
- **Generierung von Glückszahlen**: Die App kann neue Glückszahlen generieren, wobei bereits gezogene Zahlen ausgeschlossen werden.
- **Benachrichtigung beim Schließen der App**: Bevor du die App schließt, wird eine Bestätigung angefordert, um sicherzustellen, dass du das Schließen der App wirklich wünschst.
- **Einfache Installation**: Die App kann schnell und unkompliziert installiert werden.

## Klonen
   ```bash
   git clone https://github.com/MGuenther-build/EurojackpotApp.git
   ```

## Start der App
   ``` bash
   Gui_EJ.py
   ```

# Nutzung

## Zahlen eintragen

Jede gezogene Eurojackpot-Zahl kann direkt in die Datenbank eingetragen werden. Die App zeigt dir an, wann die letzte Zahl eingetragen wurde.

## Tipps vergleichen

Du kannst deine eigenen Tipps eingeben und die App prüft, ob diese bereits gezogen wurden. Bei Übereinstimmung erhältst du eine entsprechende Benachrichtigung.

## Glückszahlen generieren

Die App kann neue Glückszahlen generieren und dabei bereits gezogene Zahlen ausschließen.

## Fehlerüberprüfung

Deine eingegebenen Tipps werden auf folgende Kriterien überprüft:

* Gültiger Zahlenbereich
* Keine doppelten Zahlen
* Korrekte Unterscheidung zwischen Hauptzahlen und Zusatzzahlen

## Schließen der App

Bevor du die App schließt, wirst du gefragt, ob du dies wirklich tun möchtest.

# Technologie

* Python: Die Programmiersprache für die Implementierung der App.
* Qt: Für die grafische Benutzeroberfläche.
* SQLite: Zur Speicherung der gezogenen Eurojackpot-Zahlen.
* PyQt: Für die Integration von Qt in Python.

# Lizenz

Diese App hat keine Lizenz. Sie kann jeder herunterladen oder klonen und verändern, wie er will! Ich bin dann allerdings nicht mehr Teil solcher Projekte.

# Autoren

Martin Günther
