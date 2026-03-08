import json
import os
import time
from datetime import datetime

FILENAME = "notizen.json"
HELP_FILENAME = "help.json"
BLAU = "\033[0;38;5;110m"
ROT = "\033[5;38;5;160m"
FETT = "\033[1m"
MEMEX = BLAU + FETT
ENDE = "\033[0m"
VERSION = "1.8"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def get_sort_key(titel, notizen_dict):
    zeit_str = notizen_dict[titel].get("aktiv", "01.01.2000 00:00")
    try:
        return datetime.strptime(zeit_str, "%d.%m.%Y %H:%M")
    except ValueError:
        return datetime(2000, 1, 1)


def sort_titles(notizen):
    return sorted(notizen.keys(), key=lambda x: get_sort_key(x, notizen), reverse=True)


def load_notes(filename):
    erster_start = not os.path.exists(filename)
    if erster_start:
        return {}, True

    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f), False
    except json.JSONDecodeError:
        print(f"{ROT}Warnung: {filename} war beschädigt und wurde zurückgesetzt.{ENDE}")
        time.sleep(1.5)
        return {}, False


def save_notes(filename, notizen):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(notizen, f, indent=4, ensure_ascii=False)


def load_help_entries(filename):
    if not os.path.exists(filename):
        return None

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

    return data if isinstance(data, dict) else None


def show_welcome_if_first_start(erster_start):
    if not erster_start:
        return

    clear_screen()
    print(f"\n     Willkommen bei {MEMEX}MEMEX{ENDE} 👋")
    print("     Hier kannst du schnell Notizen anlegen, lesen und verwalten.")
    print(f"     {FETT}Tipp:{ENDE} Mit {BLAU}[+]{ENDE} erstellst du direkt deine erste Notiz.")
    print(
        f"     {FETT}Bedienungshilfe:{ENDE} Erst die Funktion, wie {BLAU}[+]{ENDE}, {BLAU}[-]{ENDE} ..\n"
        f"     dann {BLAU}[Enter]{ENDE} zur Bestätigung ..\n"
        "     danach der Aufforderung Folgen"
    )
    input(f"\n {BLAU}                       (Enter zum Starten){ENDE}")


def list_notes(notizen):
    anzahl = len(notizen)
    status = "Digitales Text-Archiv" if anzahl == 0 else f"{anzahl} {'Notiz' if anzahl == 1 else 'Notizen'} geladen"

    top_line = f"{MEMEX}MEMEX v{VERSION}{ENDE} | {status}"
    print(top_line)
    print("-" * len(top_line))

    if not notizen:
        print("\n(Keine Notizen vorhanden)")
        return

    heute = datetime.now().strftime("%d.%m.%Y")
    for i, titel in enumerate(sort_titles(notizen), 1):
        vollzeit = notizen[titel].get("aktiv", "---")
        if vollzeit != "---":
            datum_part = vollzeit[:10]
            uhrzeit_part = vollzeit[11:]
            anzeige_zeit = uhrzeit_part if datum_part == heute else datum_part
        else:
            anzeige_zeit = "---"
        print(f"{i}. {titel} {BLAU}({anzeige_zeit}){ENDE}")


def get_title_by_number(notizen, nr):
    if not nr.isdigit():
        return None, "Bitte gib eine gültige Zahl ein."

    index = int(nr) - 1
    titel_liste = sort_titles(notizen)
    if not titel_liste:
        return None, "Keine Notizen vorhanden."

    if 0 <= index < len(titel_liste):
        return titel_liste[index], None
    return None, f"Ungültige Nummer. Bitte 1 bis {len(titel_liste)} verwenden."


def read_note(notizen):
    nr = input(f"{BLAU}Nummer zum Lesen:{ENDE} ")
    titel, fehler = get_title_by_number(notizen, nr)
    if titel is None:
        print(fehler)
        time.sleep(0.8)
        return

    data = notizen[titel]
    text = data["text"]
    groesse = len(text.encode("utf-8"))
    label = "Erstellt:" if data["update"] == "nie" else "Update:"

    header_notiz = f"-- {titel} | {groesse} Bytes | {label} {data['aktiv']} --"
    print(f"\n{header_notiz}")
    print("-" * len(header_notiz))
    print()
    for zeile in text.splitlines():
        print(f"   {zeile}")
    input(f"\n{BLAU}(Enter zum Zurückkehren){ENDE}")


def delete_note(notizen, filename):
    nr = input(f"{BLAU}Nummer zum Löschen:{ENDE} ")
    titel_zu_loeschen, fehler = get_title_by_number(notizen, nr)
    if titel_zu_loeschen is None:
        print(fehler)
        time.sleep(0.8)
        return

    bestaetigung = input(f"{ROT}Wirklich löschen{ENDE} '{titel_zu_loeschen}'? [j/N]: ").strip().lower()
    if bestaetigung not in ("j", "ja", "y", "yes"):
        print("Löschen abgebrochen.")
        time.sleep(0.8)
        return

    del notizen[titel_zu_loeschen]
    save_notes(filename, notizen)
    print(f"'{titel_zu_loeschen}' gelöscht.")
    time.sleep(0.8)


def search_notes(notizen):
    suchtext = input(f"{BLAU}Suchbegriff im Titel:{ENDE} ").strip()
    if not suchtext:
        print("Bitte einen Suchbegriff eingeben.")
        time.sleep(0.8)
        return

    treffer = [titel for titel in sort_titles(notizen) if suchtext.lower() in titel.lower()]

    print(f"\nTreffer für '{suchtext}':")
    if not treffer:
        print("(Keine passenden Notizen)")
    else:
        for i, titel in enumerate(treffer, 1):
            print(f"{i}. {titel}")

    input(f"\n{BLAU}(Enter zum Zurückkehren){ENDE}")


def create_or_edit_note(notizen, filename):
    titel = input(f"{BLAU}Titel:{ENDE} ").strip()
    if not titel:
        print("Titel darf nicht leer sein.")
        time.sleep(0.8)
        return

    neue_zeilen = []
    jetzt = datetime.now().strftime("%d.%m.%Y %H:%M")

    if titel in notizen:
        print(f"\n{BLAU}Edit:{ENDE} {titel}")
        alte_zeilen = notizen[titel]["text"].split("\n")
        for i, zeile in enumerate(alte_zeilen, 1):
            edit = input(f"L{i} [{zeile}]: ")
            neue_zeilen.append(zeile if edit == "" else edit)
        print("-" * 20)
        erstellt_datum = notizen[titel].get("erstellt", jetzt)
        update_datum = jetzt
    else:
        print(f"{BLAU}Inhalt (2x Enter zum Speichern):{ENDE}")
        erstellt_datum = jetzt
        update_datum = "nie"

    while True:
        z = input()
        if z == "":
            break
        neue_zeilen.append(z)

    finaler_text = "\n".join(neue_zeilen)
    aktiv_datum = erstellt_datum if update_datum == "nie" else update_datum
    notizen[titel] = {
        "text": finaler_text,
        "erstellt": erstellt_datum,
        "update": update_datum,
        "aktiv": aktiv_datum,
    }
    save_notes(filename, notizen)
    print(f"{BLAU}Gespeichert!{ENDE}")
    time.sleep(0.8)


def show_help(help_filename):
    eintraege = load_help_entries(help_filename)

    print(f"\n{FETT}Hilfe / Befehle{ENDE}")
    print("-" * 40)
    print(f"{BLAU}[+]{ENDE}  Neue Notiz erstellen oder bestehende bearbeiten")
    print(f"{BLAU}[#]{ENDE}  Notiz über ihre Nummer lesen")
    print(f"{BLAU}[s]{ENDE}  Notizen nach Titel durchsuchen")
    print(f"{BLAU}[-]{ENDE}  Notiz über ihre Nummer löschen (mit Bestätigung)")
    print(f"{BLAU}[?]{ENDE}  Diese Hilfe anzeigen")
    print(f"{BLAU}[x]{ENDE}  Programm beenden")

    if eintraege:
        print(f"\n{FETT}Anleitungen aus {help_filename}:{ENDE}")
        for titel, data in eintraege.items():
            text = data.get("text", "") if isinstance(data, dict) else ""
            print(f"\n• {titel}")
            if text:
                for zeile in text.splitlines():
                    print(f"  {zeile}")
    else:
        print("\n(Tipp: Lege eine help.json an, um eigene Hilfetexte mitzuliefern.)")

    input(f"\n{BLAU}(Enter zum Zurückkehren){ENDE}")


def main():
    notizen, erster_start = load_notes(FILENAME)
    show_welcome_if_first_start(erster_start)

    while True:
        clear_screen()
        list_notes(notizen)
        print(f"\n{BLAU}[+] Neu/Edit  [#] Lesen  [s] Suchen  [-] Löschen  [?] Help  [x] Exit{ENDE}")
        auswahl = input(f"{BLAU}> {ENDE}").strip().lower()

        if auswahl == "x":
            break
        if auswahl == "#":
            read_note(notizen)
        elif auswahl == "s":
            search_notes(notizen)
        elif auswahl == "-":
            delete_note(notizen, FILENAME)
        elif auswahl == "+":
            create_or_edit_note(notizen, FILENAME)
        elif auswahl == "?":
            show_help(HELP_FILENAME)
        elif auswahl == "":
            continue
        else:
            print("Befehl unbekannt.")
            time.sleep(0.5)

    print(f"\n{MEMEX}MEMEX{ENDE}{FETT} | Daten sind gespeichert{ENDE}")


if __name__ == "__main__":
    main()
