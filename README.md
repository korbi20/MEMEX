# MEMEX

Ein kleines, terminalbasiertes Notiz-Archiv in Python.

Mit **MEMEX** kannst du Notizen direkt in der Konsole erstellen, bearbeiten, lesen und löschen. Alle Daten werden lokal in einer JSON-Datei gespeichert.

## Features

- 📒 Notizen lokal speichern (`notizen.json`)
- ➕ Neue Notizen anlegen
- ✏️ Bestehende Notizen zeilenweise bearbeiten
- 🔎 Notizen nach Nummer auswählen und lesen
- 🗑️ Notizen löschen
- 📏 Byte-Anzeige pro Notizinhalt
- 🔤 Sortierte Anzeige aller Notiz-Titel

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

## Projektstruktur

```text
MEMEX/
├── main.py
├── LICENSE.md
└── README.md
```

## Hinweise

- Die Anwendung speichert automatisch nach jedem Erstellen, Bearbeiten oder Löschen.
- Wenn `notizen.json` noch nicht existiert, wird sie beim ersten Speichern angelegt.

## Lizenz

Dieses Repository steht unter der **MIT License**.

- Das Projekt ist ein persönliches Showcase-/Inspiration-Projekt.
- Nutzung, Forks und Anpassungen sind unter den MIT-Bedingungen erlaubt.
- Die Software wird "as is" ohne Gewährleistung bereitgestellt.

Siehe [`LICENSE`](./LICENSE.md).
