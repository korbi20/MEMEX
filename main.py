import json
import os
import time
from datetime import datetime

FILENAME = "notizen.json"
BLAU = "\033[0;38;5;110m"
ROT = "\033[5;38;5;160m"
FETT = "\033[1m"
MEMEX = BLAU + FETT
ENDE = "\033[0m"
Version = "1.6"

def get_sort_key(titel, notizen_dict):
    zeit_str = notizen_dict[titel].get("aktiv", "01.01.2000 00:00")
    try:
        return datetime.strptime(zeit_str, "%d.%m.%Y %H:%M")
    except:
        return datetime(2000, 1, 1)

erster_start = not os.path.exists(FILENAME)

if not erster_start:
    try:
        with open(FILENAME, "r") as f:
            notizen = json.load(f)
    except json.JSONDecodeError:
        print(f"{ROT}Warnung: {FILENAME} war beschädigt und wurde zurückgesetzt.{ENDE}")
        time.sleep(1.5)
        notizen = {}
else:
    notizen = {}
    
if erster_start:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n     Willkommen bei {MEMEX}MEMEX{ENDE} 👋")
    print("     Hier kannst du schnell Notizen anlegen, lesen und verwalten.")
    print(f"     {FETT}Tipp:{ENDE} Mit {BLAU}[+]{ENDE} erstellst du direkt deine erste Notiz.")
    print(f"     {FETT}Bedienungshilfe:{ENDE} Erst die Funktion, wie {BLAU}[+]{ENDE}, {BLAU}[-]{ENDE} ..\n     dann {BLAU}[Enter]{ENDE} zur Bestätigung ..\n     danach der Aufforderung Folgen")
    input(f"\n {BLAU}                       (Enter zum Starten){ENDE}")


while True:
    os.system('cls' if os.name == 'nt' else 'clear')

    anzahl = len(notizen)
    status = "Digitales Text-Archiv" if anzahl == 0 else f"{anzahl} {'Notiz' if anzahl == 1 else 'Notizen'} geladen"

    top_line = f"{MEMEX}MEMEX v{Version}{ENDE} | {status}"
    print(top_line)
    print("-" * len(top_line))
    
    if not notizen:
        print("\n(Keine Notizen vorhanden)")
    else:
        heute = datetime.now().strftime("%d.%m.%Y")
        titel_liste = sorted(notizen.keys(), key=lambda x: get_sort_key(x, notizen), reverse=True)
        
        for i, titel in enumerate(titel_liste, 1):
            vollzeit = notizen[titel].get("aktiv", "---")
            if vollzeit != "---":
                datum_part = vollzeit[:10]
                uhrzeit_part = vollzeit[11:]
                anzeige_zeit = uhrzeit_part if datum_part == heute else datum_part
            else:
                anzeige_zeit = "---"
            print(f"{i}. {titel} {BLAU}({anzeige_zeit}){ENDE}")

    print(f"\n{BLAU}[+] Neu/Edit  [#] Lesen  [-] Löschen  [x] Exit{ENDE}")
    auswahl = input(f"{BLAU}> {ENDE}").strip().lower()

    if auswahl == "x":
        break

    elif auswahl == "#":
        nr = input(f"{BLAU}Nummer zum Lesen:{ENDE} ")
        if nr.isdigit():
            index = int(nr) - 1
            titel_liste = sorted(notizen.keys(), key=lambda x: get_sort_key(x, notizen), reverse=True)
            if 0 <= index < len(titel_liste):
                titel = titel_liste[index]
                data = notizen[titel]
                text = data["text"]
                groesse = len(text.encode('utf-8'))
                label = "Erstellt:" if data["update"] == "nie" else "Update:"
                
                header_notiz = f"-- {titel} | {groesse} Bytes | {label} {data['aktiv']} --"
                print(f"\n{header_notiz}")
                print("-" * len(header_notiz))
                print()
                for zeile in text.splitlines():
                    print(f"   {zeile}")
                input(f"\n{BLAU}(Enter zum Zurückkehren){ENDE}")
            else:
                print("Ungültige Nummer!")
                time.sleep(0.5)

    elif auswahl == "-":
        nr = input(f"{BLAU}Nummer zum Löschen:{ENDE} ")
        if nr.isdigit():
            index = int(nr) - 1
            titel_liste = sorted(notizen.keys(), key=lambda x: get_sort_key(x, notizen), reverse=True)
            if 0 <= index < len(titel_liste):
                titel_zu_loeschen = titel_liste[index]
                del notizen[titel_zu_loeschen]
                with open(FILENAME, "w") as f:
                    json.dump(notizen, f, indent=4)
                print(f"'{titel_zu_loeschen}' gelöscht.")
            else:
                print("Ungültige Nummer!")
        time.sleep(0.8)

    elif auswahl == "+":
        titel = input(f"{BLAU}Titel:{ENDE} ")
        if titel:
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
                if z == "": break
                neue_zeilen.append(z)
            
            finaler_text = "\n".join(neue_zeilen)
            aktiv_datum = erstellt_datum if update_datum == "nie" else update_datum
            notizen[titel] = {"text": finaler_text, "erstellt": erstellt_datum, "update": update_datum, "aktiv": aktiv_datum}
            with open(FILENAME, "w") as f:
                json.dump(notizen, f, indent=4)
            print(f"{BLAU}Gespeichert!{ENDE}")
        time.sleep(0.8)

    elif auswahl == "":
        continue
    else:
        print("Befehl unbekannt.")
        time.sleep(0.5)

print(f"\n{MEMEX}MEMEX{ENDE}{FETT} | Daten sind gespeichert{ENDE}")
