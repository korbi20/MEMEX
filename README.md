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
> - Optional kannst du eine `help.json` mit eigenen Hilfetexten mitliefern (Beispieldatei im Repo).

## Lizenz

Dieses Repository steht unter der **MIT License**.

- Das Projekt ist ein persönliches Showcase-/Inspiration-Projekt.
- Nutzung, Forks und Anpassungen sind unter den MIT-Bedingungen erlaubt.
- Die Software wird "as is" ohne Gewährleistung bereitgestellt.

Siehe [`LICENSE`](./LICENSE.md).
