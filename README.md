# EurojackpotApp

**EurojackpotApp** ist eine Python-basierte Anwendung, die es Ihnen ermöglicht gezogenen Eurojackpot-Zahlen zu verwalten, Tipps zu vergleichen und neue Glückszahlen zu generieren. Die App nutzt Qt für die grafische Benutzeroberfläche und SQLite für die Speicherung der gezogenen Zahlen.

## Features
- **Datenbank der gezogenen Zahlen**: Alle jemals gezogenen Eurojackpot-Zahlen werden in einer SQLite-Datenbank gespeichert.
- **Vergleich deiner Tipps**: Sie können eigene Tipps mit den bereits gezogenen Zahlen vergleichen. Eine Benachrichtigung wird angezeigt, wenn Ihr Tipp bereits gezogen wurde.
- **Fehlerüberprüfung**: Ihre Tipps werden auf Fehler überprüft, z.B. ob die Zahlen im gültigen Bereich liegen und ob es doppelte Zahlen gibt. Es wird zwischen Hauptzahlen und Zusatzzahlen unterschieden.
- **Generierung von Glückszahlen**: Die App kann neue Glückszahlen generieren, wobei bereits gezogene Zahlen ausgeschlossen werden.
- **Benachrichtigung beim Schließen der App**: Bevor Sie die App schließen, wird eine Bestätigung angefordert, um sicherzustellen, dass das Schließen der App auch wirklich erwünschst ist.
- **Einfache Installation**: Die App kann schnell und unkompliziert installiert werden.

## Klonen
   ```bash
   git clone https://github.com/MGuenther-build/EurojackpotApp.git
   ```

## Start der App
   ``` bash
   main.py
   ```

# Nutzung

## Zahlen eintragen
Jede gezogene Eurojackpot-Zahl kann direkt in die Datenbank eingetragen werden. Die App zeigt an, wann die letzte Zahlen eingetragen wurden.

## Tipps vergleichen
Sie können eigene Tipps eingeben und die App prüft, ob diese bereits gezogen wurden. Bei Übereinstimmung erhalten Sie eine entsprechende Benachrichtigung.

## Glückszahlen generieren
Die App kann neue Glückszahlen generieren und dabei bereits gezogene Zahlen ausschließen.

## Fehlerüberprüfung
Eingegebene Tipps werden auf folgende Kriterien überprüft:
* Gültiger Zahlenbereich
* Keine doppelten Zahlen
* Korrekte Unterscheidung zwischen Hauptzahlen und Zusatzzahlen

## Schließen der App
Bevor Sie die App schließen, werden Sie gefragt, ob Sie dies wirklich tun möchten.

# Technologie
* Python: Die Programmiersprache für die Implementierung der App.
* Qt: Für die grafische Benutzeroberfläche.
* SQLite: Zur Speicherung der gezogenen Eurojackpot-Zahlen.
* PyQt: Für die Integration von Qt in Python.

# Responsivität
Dieses Programm ist auf Desktop-PCs responsiv, es ist aber nicht für die Handynutzung geeignet.

# Lizenz
Diese App unterliegt der MIT-Lizenz. Sie kann von Jedem herunterladen oder geklont werden und dann natürlich auch verändert/erweitert werden! Ich bin dann allerdings nicht mehr Teil solcher Projekte.

# Autor
Martin Günther

# Link zum Projekt
https://www.mguenther-build.de/portfolio
