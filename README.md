# MEMEX

Ein kleines, terminalbasiertes Notiz-Archiv in Python.

Mit **MEMEX** kannst du Notizen direkt in der Konsole erstellen, bearbeiten, lesen und löschen. Alle Daten werden lokal in einer JSON-Datei gespeichert.

## Zweck / Status

- Persönliches Terminal-Projekt zum schnellen Notieren von Ideen.
- Öffentlich auf GitHub als Showcase und Inspiration.
- Kein Produkt-Support oder SLA — Nutzung auf eigene Verantwortung.

## Voraussetzungen

- Python **3.8+** (empfohlen)
- Keine externen Abhängigkeiten (nur Standardbibliothek)

## Installation / Start

1. Repository klonen oder Dateien herunterladen.
2. Ins Projektverzeichnis wechseln.
3. Anwendung starten:

```bash
python3 main.py
```

> Unter Windows ggf. `python main.py` verwenden.

## Bedienung

Nach dem Start siehst du eine Übersicht der vorhandenen Notizen und folgende Befehle:

- `[+]` **Neu/Edit** – neue Notiz anlegen oder bestehende bearbeiten
- `[#]` **Lesen** – Notiz über ihre Nummer anzeigen
- `[-]` **Löschen** – Notiz über ihre Nummer entfernen
- `[x]` **Exit** – Programm beenden

### Bearbeitungsmodus

Wenn du einen vorhandenen Titel erneut auswählst, startet der Edit-Modus:

- Leere Eingabe bei einer Zeile → bestehende Zeile bleibt erhalten
- Text eingeben → Zeile wird ersetzt
- Danach können zusätzliche Zeilen ergänzt werden
- Mit einer leeren Zeile wird gespeichert

## Datenformat

Alle Notizen werden in der Datei `notizen.json` gespeichert – als Key-Value-Paare:

- **Key:** Titel der Notiz
- **Value:** Inhalt der Notiz (mehrzeilig möglich)

Beispiel:

```json
{
  "Einkauf": "Milch\nBrot\nKaffee",
  "Ideen": "Terminal-App verbessern"
}
```

> ## Hinweise
> - Die Anwendung speichert automatisch nach jedem Erstellen, Bearbeiten oder Löschen.
> - Wenn `notizen.json` noch nicht existiert, wird sie beim ersten Speichern angelegt.
> - Notizen bleiben lokal im Projektordner (`notizen.json`).

## Lizenz

Dieses Repository steht unter der **MIT License**.

- Das Projekt ist ein persönliches Showcase-/Inspiration-Projekt.
- Nutzung, Forks und Anpassungen sind unter den MIT-Bedingungen erlaubt.
- Die Software wird "as is" ohne Gewährleistung bereitgestellt.

Siehe [`LICENSE`](./LICENSE.md).

## Mini-Roadmap

### v1.7 – Stabilität & Struktur

- Interne Funktionen aus dem Hauptloop auslagern (`anzeigen`, `lesen`, `löschen`, `speichern`), um Wartbarkeit zu verbessern.
- Fehlerbehandlung beim Datums-Parsing präzisieren (`except ValueError` statt allgemeinem `except`).
- Konsistente UTF-8-Dateioperationen (`encoding="utf-8"`) beim Lesen/Schreiben der JSON-Datei.

### v1.8 – UX-Verbesserungen

- Bestätigungsabfrage vor dem Löschen einer Notiz.
- Optionales Such-/Filterkommando für Titel.
- Verbesserte Eingabehinweise bei ungültigen Nummern oder leeren Titeln.

### v2.0 – Produktiv nutzbare Basis

- Backup/Restore (`notizen.backup.json`) und optional Export (`.txt`/`.md`).
- Kleine Test-Suite für Kernfunktionen (Laden, Speichern, Sortierung, Edit-Pfade).
- Optionaler `--datei`-Parameter für alternative Speicherdateien (z. B. getrennte Bereiche Arbeit/Privat).
