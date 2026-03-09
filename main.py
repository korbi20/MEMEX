import json
import os
import time
import shutil
import re
from datetime import datetime

FILENAME = "notizen.json"
VERSION = "2.0"
TERMINAL_WIDTH = 75
TERMINAL_HEIGHT = 25
ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")

BLAU = "\033[0;38;5;110m"
ROT = "\033[5;38;5;160m"
FETT = "\033[1m"
MEMEX = BLAU + FETT
ENDE = "\033[0m"

# Terminal Utility Functions

def visible_len(text):
    return len(ANSI_ESCAPE_RE.sub("", text))

def set_terminal_size(width=TERMINAL_WIDTH, height=TERMINAL_HEIGHT):
    try:
        if os.name == "nt":
            os.system(f"mode con: cols={width} lines={height}")
        elif os.isatty(0):
            os.system(f"stty cols {width} rows {height}")
    except OSError:
        pass

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_lr(left, right, width=None):
    if width is None:
        width = shutil.get_terminal_size(fallback=(TERMINAL_WIDTH, TERMINAL_HEIGHT)).columns
    gap = max(1, width - visible_len(left) - visible_len(right))
    print(f"{left}{' ' * gap}{right}")

def print_center(text, width=None):
    if width is None:
        width = shutil.get_terminal_size(fallback=(TERMINAL_WIDTH, TERMINAL_HEIGHT)).columns
    pad = max(0, (width - visible_len(text)) // 2)
    print(" " * pad + text)

def print_lcr(left, center, right, width=None):
    if width is None:
        width = shutil.get_terminal_size(fallback=(TERMINAL_WIDTH, TERMINAL_HEIGHT)).columns

    left_len = visible_len(left)
    center_len = visible_len(center)
    right_len = visible_len(right)

    total_len = left_len + center_len + right_len
    if total_len >= width:
        print(f"{left} {center} {right}")
        return

    free_space = width - total_len
    left_gap = free_space // 2
    right_gap = free_space - left_gap

    print(f"{left}{' ' * left_gap}{center}{' ' * right_gap}{right}")

def get_sort_key(titel, notizen_dict):
    zeit_str = notizen_dict[titel].get("aktiv", "01.01.2000 00:00")
    try:
        return datetime.strptime(zeit_str, "%d.%m.%Y %H:%M")
    except ValueError:
        return datetime(2000, 1, 1)

def sort_titles(notizen):
    return sorted(notizen.keys(), key=lambda x: get_sort_key(x, notizen), reverse=True)

# Data Handling Functions

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

def show_welcome_if_first_start(erster_start):
    if not erster_start:
        return

    clear_screen()
    print_center(f"Willkommen bei {MEMEX}MEMEX{ENDE} 👋")
    print_center("Hier kannst du schnell Notizen anlegen, lesen und verwalten.")
    print_center(f"{FETT}Tipp:{ENDE} Mit {BLAU}[+]{ENDE} erstellst du direkt deine erste Notiz.")
    print()
    print_center(f"{FETT}Bedienungshilfe:{ENDE} Erst die Funktion, dann {BLAU}[Enter]{ENDE} bestätigen")
    print_center(f"Danach den Anweisungen folgen")
    print()
    print_center(f"{BLAU}(Enter zum Starten){ENDE}")
    input()

def list_notes(notizen):
    anzahl = len(notizen)
    status = "Digitales Text-Archiv" if anzahl == 0 else f"{anzahl} {'Notiz' if anzahl == 1 else 'Notizen'} geladen"
    function_current = "Notizenübersicht"

    left = f"{MEMEX}MEMEX v{VERSION}{ENDE}"
    right = status
    center = function_current
    breite = shutil.get_terminal_size(fallback=(TERMINAL_WIDTH, TERMINAL_HEIGHT)).columns
    print_lcr(left, center, right, breite)
    print("-" * breite)

    if not notizen:
        print()
        print_center("(Keine Notizen vorhanden)")
        print()
        return

    heute = datetime.now().strftime("%d.%m.%Y")
    print()
    for i, titel in enumerate(sort_titles(notizen), 1):
        vollzeit = notizen[titel].get("aktiv", "---")
        if vollzeit != "---":
            datum_part = vollzeit[:10]
            uhrzeit_part = vollzeit[11:]
            anzeige_zeit = uhrzeit_part if datum_part == heute else datum_part
        else:
            anzeige_zeit = "---"
        print(f"    {i}. {titel} {BLAU}({anzeige_zeit}){ENDE}")

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

# Note Functions

def read_note(notizen):
    nr = input(f"{BLAU}Nummer zum Lesen:{ENDE} ")
    titel, fehler = get_title_by_number(notizen, nr)
    if titel is None:
        print()
        print_center(fehler)
        time.sleep(0.8)
        return

    data = notizen[titel]
    text = data["text"]
    groesse = len(text.encode("utf-8"))
    label = "Erstellt:" if data["update"] == "nie" else "Update:"
    header_notiz = f"-- {titel} | {groesse} Bytes | {label} {data['aktiv']} --"
    clear_screen()

    left = f"{MEMEX}MEMEX v{VERSION}{ENDE}"
    right = "Notizenleser"
    breite = shutil.get_terminal_size(fallback=(TERMINAL_WIDTH, TERMINAL_HEIGHT)).columns
    print_lr(left, right, breite)
    print("-" * breite)
    print()

    print_center(f"{header_notiz}")
    print()
    for zeile in text.splitlines():
        print(f"   {zeile}")
    print()
    print_center(f"{BLAU}(Enter zum Zurückkehren){ENDE}")
    input()

def delete_note(notizen, filename):
    nr = input(f"{BLAU}Nummer zum Löschen:{ENDE} ")
    titel_zu_loeschen, fehler = get_title_by_number(notizen, nr)
    if titel_zu_loeschen is None:
        print()
        print_center(fehler)
        time.sleep(0.8)
        return

    bestaetigung = input(f"{ROT}Wirklich löschen{ENDE} '{titel_zu_loeschen}'{ROT}? [j/N]:{ENDE} ").strip().lower()
    print()
    if bestaetigung not in ("j", "ja", "y", "yes"):
        print_center("Löschen abgebrochen.")
        time.sleep(0.8)
        return

    del notizen[titel_zu_loeschen]
    save_notes(filename, notizen)
    print_center(f"'{titel_zu_loeschen}' gelöscht.")
    time.sleep(0.8)

def search_notes(notizen):
    suchtext = input(f"{BLAU}Suchbegriff im Titel:{ENDE} ").strip()
    if not suchtext:
        print_center("Bitte einen Suchbegriff eingeben.")
        time.sleep(0.8)
        return

    treffer = [titel for titel in sort_titles(notizen) if suchtext.lower() in titel.lower()]
    
    clear_screen()
    
    left = f"{MEMEX}MEMEX v{VERSION}{ENDE}"
    right = "Suche"
    breite = shutil.get_terminal_size(fallback=(TERMINAL_WIDTH, TERMINAL_HEIGHT)).columns
    print_lr(left, right, breite)
    print("-" * breite)
    print()
    
    print(f"{BLAU}Treffer für '{ENDE}{suchtext}{BLAU}':{ENDE}")
    print()
    if not treffer:
        print_center("(Keine passenden Notizen)")
    else:
        for i, titel in enumerate(treffer, 1):
            print(f"    {i}. {titel}")

    print()
    print_center(f"{BLAU}(Enter zum Zurückkehren){ENDE}")
    input()

def create_or_edit_note(notizen, filename):
    clear_screen()

    left = f"{MEMEX}MEMEX v{VERSION}{ENDE}"
    right = "Editor"
    breite = shutil.get_terminal_size(fallback=(TERMINAL_WIDTH, TERMINAL_HEIGHT)).columns
    print_lr(left, right, breite)
    print("-" * breite)
    print()

    titel = input(f"{BLAU}Titel:{ENDE} ").strip()
    if not titel:
        print_center("Titel darf nicht leer sein.")
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
    print_center(f"{BLAU}Gespeichert!{ENDE}")
    time.sleep(0.8)

def show_help():
    clear_screen()
    left = f"{MEMEX}MEMEX v{VERSION}{ENDE}"
    right = "Hilfecenter"
    breite = shutil.get_terminal_size(fallback=(TERMINAL_WIDTH, TERMINAL_HEIGHT)).columns
    print_lr(left, right, breite)
    print("-" * breite)
 
    print(f"\n  {FETT}Hilfe / Befehle{ENDE}")
    print("-" * 40)
    print(f"    {BLAU}[+]{ENDE}  Neue Notiz erstellen oder bestehende bearbeiten")
    print(f"    {BLAU}[#]{ENDE}  Notiz über ihre Nummer lesen")
    print(f"    {BLAU}[s]{ENDE}  Notizen nach Titel durchsuchen")
    print(f"    {BLAU}[-]{ENDE}  Notiz über ihre Nummer löschen (mit Bestätigung)")
    print(f"    {BLAU}[?]{ENDE}  Diese Hilfe anzeigen")
    print(f"    {BLAU}[x]{ENDE}  Programm beenden")

    print(f"\n  {FETT}Vorgehensweise:{ENDE}")
    print("-" * 40)
    print(f"    {BLAU}1.{ENDE}  Funktion auswählen (Bsp. '{BLAU}+{ENDE}')")
    print(f"    {BLAU}2.{ENDE}  mit {BLAU}Enter{ENDE} bestätigen")
    print(f"    {BLAU}3.{ENDE}  folge den {BLAU}Anweisungen{ENDE}")
    print(f"\n    {BLAU}//{ENDE}  mit {BLAU}Enter{ENDE} immer bestätigen, außer es wird anders {BLAU}angegeben{ENDE}")
    print(f"    {BLAU}//{ENDE}  mit {BLAU}Enter{ENDE} kann eine Versehene Funktion {BLAU}abgebrochen{ENDE} werden")

    print()
    print_center(f"{BLAU}(Enter zum Zurückkehren){ENDE}")
    input()

# Main Loop

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
            show_help()
        elif auswahl == "":
            continue
        else:
            print_center("Befehl unbekannt.")
            time.sleep(0.5)

    print_center(f"{MEMEX}MEMEX{ENDE}{FETT} | Daten sind gespeichert{ENDE}")

if __name__ == "__main__":
    main()
