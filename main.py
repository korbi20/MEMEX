import json
import os
import time

FILENAME = "notizen.json"

if os.path.exists(FILENAME):
    with open(FILENAME, "r") as f:
        notizen = json.load(f)
else:
    notizen = {}

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"MEMEX v1.0 | Digitales Text-Archiv")
    print("---------------------------------")
    if not notizen:
        print("(Keine Notizen vorhanden)")
    else:
        for i, titel in enumerate(notizen.keys(), 1):
            print(f"{i}. {titel}")

    print("\n[+] Name tippen = Neue Notiz")
    print("[#] Nummer tippen = Lesen")
    print("[-] 'del' + Nummer = Löschen (z.B. del 1)")
    print("[x] 'exit' = Beenden")

    auswahl = input("\nWas willst du tun? ").strip()

    if auswahl.lower() == "exit":
        break

    elif auswahl.isdigit():
        index = int(auswahl) - 1
        titel_liste = list(notizen.keys())
        if 0 <= index < len(titel_liste):
            print(f"\n--- {titel_liste[index]} ---")
            print(notizen[titel_liste[index]])
            input("\n(Enter zum Zurückkehren)")
        else:
            print("Ungültige Nummer!")
            time.sleep(1.5) # Kurze Pause zum Lesen

    elif auswahl.startswith("del "):
        try:
            nr = int(auswahl.split()[1]) - 1
            titel_zu_loeschen = list(notizen.keys())[nr]
            del notizen[titel_zu_loeschen]
            print(f"'{titel_zu_loeschen}' gelöscht.")
            # Wichtig: Speichern nach dem Löschen!
            with open(FILENAME, "w") as f:
                json.dump(notizen, f, indent=4)
        except:
            print("Fehler! Nutze z.B. 'del 1'")
        time.sleep(1.5)

    elif auswahl == "": # Verhindert leere Eingaben
        continue

    else:
        titel = auswahl
        text = input(f"Inhalt für '{titel}': ")
        notizen[titel] = text
        with open(FILENAME, "w") as f:
            json.dump(notizen, f, indent=4)
        print("Gespeichert!")
        time.sleep(1)

print("Programm beendet.")
