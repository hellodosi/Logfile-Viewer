# Logfile-Viewer

`Logfile-Viewer` ist ein schnelles und portables Werkzeug für Windows zur Analyse von Logdateien. Es wurde als Stand-Alone-Anwendung konzipiert, die keine Installation erfordert und direkt von einem USB-Stick oder einem Netzlaufwerk aus gestartet werden kann. Alle Einstellungen werden in einer einzigen Konfigurationsdatei im Programmverzeichnis gespeichert.

Die Anwendung bietet eine übersichtliche Oberfläche mit einer Dateibaumansicht und einem Textbereich, der Log-Einträge basierend auf benutzerdefinierten Regeln farblich hervorhebt.

<!-- Fügen Sie hier einen Screenshot der Anwendung ein -->
<!-- !Screenshot der Anwendung -->

## Hauptfunktionen (Features)

*   **Portable Anwendung:** Keine Installation notwendig. Alle Einstellungen werden lokal in einer `JSON`-Datei gespeichert, was den portablen Einsatz ermöglicht.
*   **Dateibrowser:**
    *   Strukturierte Baumansicht des ausgewählten Ordners.
    *   Durchsuchen von Unterverzeichnissen (aktivierbar).
    *   Filterung der Dateiliste nach Dateinamen.
    *   Filterung nach Dateiendungen (z.B. `.log`, `.txt`, oder auch Dateien ohne Endung).
    *   Sortierung nach Name oder Änderungsdatum.
*   **Live View:**
    *   Automatische Aktualisierung der Anzeige, wenn die ausgewählte Datei geändert wird (Echtzeit-Monitoring).
    *   "Auto-Scroll"-Funktion, die automatisch zum Ende der Datei scrollt, aber pausiert, sobald der Benutzer manuell nach oben scrollt.
*   **Anpassbare Hervorhebungen:**
    *   Erstellen Sie eigene Regeln zur farblichen Hervorhebung von Zeilen.
    *   Jede Regel kann auf mehreren Schlüsselwörtern basieren (z.B. "ERROR", "FATAL", "EXCEPTION").
    *   Definieren Sie für jede Regel eine eigene Text- und Hintergrundfarbe.
    *   Die Priorität der Regeln kann in den Einstellungen angepasst werden (obere Regeln haben Vorrang).
*   **Weitere Funktionen:**
    *   Integrierte Suchfunktion im Log-Inhalt.
    *   Aktivierbarer Zeilenumbruch ("Word Wrap").
    *   Mehrsprachige Oberfläche (Deutsch & Englisch), die sich an der Systemsprache orientiert.
    *   Verwaltung von bekannten Dateiendungen direkt in der Anwendung.

## Anwendung

1.  **Starten:** Führen Sie die `logviewer.exe` aus. Die Anwendung startet und zeigt standardmäßig die Dateien im eigenen Verzeichnis an.
2.  **Ordner öffnen:** Nutzen Sie das Menü `Datei > Ordner öffnen...`, um ein anderes Verzeichnis mit Logdateien zu laden.
3.  **Datei auswählen:** Klicken Sie auf eine Datei in der Baumansicht links, um deren Inhalt im Hauptfenster anzuzeigen.
4.  **Live View nutzen:** Aktivieren Sie die Checkbox `Live View`, um die ausgewählte Datei in Echtzeit zu überwachen.
5.  **Hervorhebungen anwenden:** Nutzen Sie die Checkboxen über dem Textbereich, um Zeilen mit bestimmten Schlüsselwörtern gemäß den konfigurierten Regeln farblich hervorzuheben.

## Konfiguration

Alle Einstellungen werden in der Datei `log_viewer_settings.json` im selben Verzeichnis wie die EXE-Datei gespeichert. Die wichtigsten Konfigurationen können bequem über das Menü `Datei > Einstellungen` vorgenommen werden:

*   **Allgemein:** Passen Sie das Verhalten des Dateibrowsers an, ändern Sie die Sprache oder verwalten Sie die für den Filter relevanten Dateiendungen.
*   **Hervorhebungen:** Verwalten Sie die Regeln für die farbliche Kennzeichnung. Erstellen Sie neue Regeln, bearbeiten oder löschen Sie bestehende und passen Sie deren Priorität an.

---
Copyright © Dominik Scharrer