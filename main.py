import json
import os
import time

FILENAME = "notizen.json"
GELB = "\033[93m"
ENDE = "\033[0m"

if os.path.exists(FILENAME):
    with open(FILENAME, "r") as f:
        notizen = json.load(f)
else:
    notizen = {}

while True:
    os.system('cls' if os.name == 'nt' else 'clear')

    anzahl = len(notizen)
    if anzahl == 0:
        header_text = "Digitales Text-Archiv"
    else:
        wort = "Notiz" if anzahl == 1 else "Notizen"
        header_text = f"{anzahl} {wort} geladen"

    print(f"MEMEX v1.1.2 | {header_text}")
    print("-" * 35)
    
    if not notizen:
        print("\n(Keine Notizen vorhanden)")
    else:
        # Sortierte Anzeige für die Übersicht
        for i, titel in enumerate(sorted(notizen.keys()), 1):
            print(f"{i}. {titel}")

    print(f"\n{GELB}[+] Neu/Edit  [#] Lesen  [-] Löschen  [x] Exit{ENDE}")
    auswahl = input("> ").strip().lower()

    if auswahl == "x":
        break

    # [#] LESEN (mit Byte-Anzeige)
    elif auswahl == "#":
        nr = input("Nummer zum Lesen: ")
        if nr.isdigit():
            index = int(nr) - 1
            titel_liste = sorted(notizen.keys())
            if 0 <= index < len(titel_liste):
                titel = titel_liste[index]
                inhalt = notizen[titel]
                
                # Größe der einzelnen Notiz in Bytes berechnen
                groesse = len(inhalt.encode('utf-8'))
                
                print(f"\n--- {titel} | {groesse} Bytes ---")
                print(inhalt)
                input("\n(Enter zum Zurückkehren)")
            else:
                print("Ungültige Nummer!")
                time.sleep(1)

    # [-] LÖSCHEN
    elif auswahl == "-":
        nr = input("Nummer zum Löschen: ")
        if nr.isdigit():
            index = int(nr) - 1
            titel_liste = sorted(notizen.keys())
            if 0 <= index < len(titel_liste):
                titel_zu_loeschen = titel_liste[index]
                del notizen[titel_zu_loeschen]
                with open(FILENAME, "w") as f:
                    json.dump(notizen, f, indent=4)
                print(f"'{titel_zu_loeschen}' gelöscht.")
            else:
                print("Ungültige Nummer!")
        time.sleep(1)

    # [+] NEU ODER BEARBEITEN
    elif auswahl == "+":
        titel = input("Titel: ")
        if titel:
            neue_zeilen = []
            if titel in notizen:
                print(f"\n{GELB}Edit: {titel}{ENDE}")
                print("(Enter = Zeile behalten | Text = Zeile ändern)")
                alte_zeilen = notizen[titel].split("\n")
                for i, zeile in enumerate(alte_zeilen, 1):
                    edit = input(f"L{i} [{zeile}]: ")
                    neue_zeilen.append(zeile if edit == "" else edit)
                print("-" * 20)
                print("Weitere Zeilen hinzufügen? (2x Enter zum Speichern)")
            else:
                print("Inhalt (2x Enter zum Speichern):")

            while True:
                z = input()
                if z == "":
                    break
                neue_zeilen.append(z)
            
            notizen[titel] = "\n".join(neue_zeilen)
            with open(FILENAME, "w") as f:
                json.dump(notizen, f, indent=4)
            print("Gespeichert!")
        time.sleep(0.8)

    elif auswahl == "":
        continue
    else:
        print("Befehl unbekannt.")
        time.sleep(1)

print("MEMEX | Daten sind gespeichert")
